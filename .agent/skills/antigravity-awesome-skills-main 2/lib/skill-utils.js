const fs = require('fs');
const path = require('path');
const yaml = require('yaml');

function stripQuotes(value) {
  if (typeof value !== 'string') return value;
  if (value.length < 2) return value.trim();
  const first = value[0];
  const last = value[value.length - 1];
  if ((first === '"' && last === '"') || (first === "'" && last === "'")) {
    return value.slice(1, -1).trim();
  }
  if (first === '"' || first === "'") {
    return value.slice(1).trim();
  }
  if (last === '"' || last === "'") {
    return value.slice(0, -1).trim();
  }
  return value.trim();
}

function parseInlineList(raw) {
  if (typeof raw !== 'string') return [];
  const value = raw.trim();
  if (!value.startsWith('[') || !value.endsWith(']')) return [];
  const inner = value.slice(1, -1).trim();
  if (!inner) return [];
  return inner
    .split(',')
    .map(item => stripQuotes(item.trim()))
    .filter(Boolean);
}

function isPlainObject(value) {
  return value && typeof value === 'object' && !Array.isArray(value);
}

function parseFrontmatter(content) {
  const sanitized = content.replace(/^\uFEFF/, '');
  const lines = sanitized.split(/\r?\n/);
  if (!lines.length || lines[0].trim() !== '---') {
    return { data: {}, body: content, errors: [], hasFrontmatter: false };
  }

  let endIndex = -1;
  for (let i = 1; i < lines.length; i += 1) {
    if (lines[i].trim() === '---') {
      endIndex = i;
      break;
    }
  }

  if (endIndex === -1) {
    return {
      data: {},
      body: content,
      errors: ['Missing closing frontmatter delimiter (---).'],
      hasFrontmatter: true,
    };
  }

  const errors = [];
  const fmText = lines.slice(1, endIndex).join('\n');
  let data = {};

  try {
    const doc = yaml.parseDocument(fmText, { prettyErrors: false });
    if (doc.errors && doc.errors.length) {
      errors.push(...doc.errors.map(error => error.message));
    }
    data = doc.toJS();
  } catch (err) {
    errors.push(err.message);
    data = {};
  }

  if (!isPlainObject(data)) {
    errors.push('Frontmatter must be a YAML mapping/object.');
    data = {};
  }

  const body = lines.slice(endIndex + 1).join('\n');
  return { data, body, errors, hasFrontmatter: true };
}

function tokenize(value) {
  if (!value) return [];
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .split(' ')
    .map(token => token.trim())
    .filter(Boolean);
}

function unique(list) {
  const seen = new Set();
  const result = [];
  for (const item of list) {
    if (!item || seen.has(item)) continue;
    seen.add(item);
    result.push(item);
  }
  return result;
}

function readSkill(skillDir, skillId) {
  const skillPath = path.join(skillDir, skillId, 'SKILL.md');
  const content = fs.readFileSync(skillPath, 'utf8');
  const { data } = parseFrontmatter(content);
  const name = typeof data.name === 'string' && data.name.trim()
    ? data.name.trim()
    : skillId;
  const description = typeof data.description === 'string'
    ? data.description.trim()
    : '';

  let tags = [];
  if (Array.isArray(data.tags)) {
    tags = data.tags.map(tag => String(tag).trim());
  } else if (typeof data.tags === 'string' && data.tags.trim()) {
    const parts = data.tags.includes(',')
      ? data.tags.split(',')
      : data.tags.split(/\s+/);
    tags = parts.map(tag => tag.trim());
  } else if (isPlainObject(data.metadata) && data.metadata.tags) {
    const rawTags = data.metadata.tags;
    if (Array.isArray(rawTags)) {
      tags = rawTags.map(tag => String(tag).trim());
    } else if (typeof rawTags === 'string' && rawTags.trim()) {
      const parts = rawTags.includes(',')
        ? rawTags.split(',')
        : rawTags.split(/\s+/);
      tags = parts.map(tag => tag.trim());
    }
  }

  tags = tags.filter(Boolean);

  return {
    id: skillId,
    name,
    description,
    tags,
    path: skillPath,
    content,
  };
}

function listSkillIds(skillsDir) {
  return fs.readdirSync(skillsDir)
    .filter(entry => {
      if (entry.startsWith('.')) return false;
      const dirPath = path.join(skillsDir, entry);
      if (!fs.statSync(dirPath).isDirectory()) return false;
      const skillPath = path.join(dirPath, 'SKILL.md');
      return fs.existsSync(skillPath);
    })
    .sort();
}

/**
 * Recursively list all skill directory paths under skillsDir (relative paths).
 * Matches generate_index.py behavior so catalog includes nested skills (e.g. game-development/2d-games).
 */
function listSkillIdsRecursive(skillsDir, baseDir = skillsDir, acc = []) {
  const entries = fs.readdirSync(baseDir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    if (!entry.isDirectory()) continue;
    const dirPath = path.join(baseDir, entry.name);
    const skillPath = path.join(dirPath, 'SKILL.md');
    const relPath = path.relative(skillsDir, dirPath);
    if (fs.existsSync(skillPath)) {
      acc.push(relPath);
    }
    listSkillIdsRecursive(skillsDir, dirPath, acc);
  }
  return acc.sort();
}

module.exports = {
  listSkillIds,
  listSkillIdsRecursive,
  parseFrontmatter,
  parseInlineList,
  readSkill,
  stripQuotes,
  tokenize,
  unique,
};
