import fs from "node:fs";
import path from "node:path";

const ensureDir=(dir)=>fs.mkdirSync(dir,{recursive:true});
const readJson=(file)=>{try{return JSON.parse(fs.readFileSync(file,"utf8"));}catch{return {};}};
const writeJson=(file,data)=>{ensureDir(path.dirname(file));fs.writeFileSync(file,`${JSON.stringify(data,null,2)}\n`);};
const stdio={command:"ag-kit",args:["mcp","serve"]};
const mergeMcp=(file,entry=stdio)=>{const data=readJson(file);data.mcpServers={...(data.mcpServers||{}),"ag-kit":entry};writeJson(file,data);return{wired:true,file};};

export function wireRuntimeMcp({root=process.cwd(),runtime}){
  const target=path.resolve(root);let result;
  if(runtime==="antigravity")result=mergeMcp(path.join(target,".agents","mcp_config.json"));
  else if(runtime==="claude")result=mergeMcp(path.join(target,".mcp.json"),{...stdio,env:{}});
  else if(runtime==="gemini")result=mergeMcp(path.join(target,".gemini","settings.json"));
  else if(runtime==="qwen")result=mergeMcp(path.join(target,".qwen","settings.json"));
  else if(runtime==="kimi")result=mergeMcp(path.join(target,".kimi-code","mcp.json"));
  else if(runtime==="cursor")result=mergeMcp(path.join(target,".cursor","mcp.json"));
  else if(runtime==="copilot")result=mergeMcp(path.join(target,".mcp.json"),{type:"local",...stdio,env:{},tools:["*"]});
  else if(runtime==="codex"){
    const pluginDir=path.join(target,".codex-plugin");const pluginSkills=path.join(pluginDir,"skills");ensureDir(pluginDir);fs.rmSync(pluginSkills,{recursive:true,force:true});const projected=path.join(target,".agents","skills");if(fs.existsSync(projected))fs.cpSync(projected,pluginSkills,{recursive:true});const mcpFile=path.join(pluginDir,".mcp.json");writeJson(mcpFile,{mcpServers:{"ag-kit":stdio}});const pluginFile=path.join(pluginDir,"plugin.json");writeJson(pluginFile,{name:"ag-kit",version:"2.0.0",description:"AG Kit shared skills and project-local MCP bridge",skills:"./skills/",mcpServers:"./.mcp.json"});return{wired:true,file:path.relative(target,mcpFile),plugin:path.relative(target,pluginFile),skills:path.relative(target,pluginSkills)};
  }else if(runtime==="openclaw")return{wired:false,reason:"Run `openclaw mcp add`/`openclaw mcp set` for the ag-kit stdio server; OpenClaw owns its MCP registry."};
  else return{wired:false,reason:"runtime has no verified project-scoped MCP projection; configure its MCP client to run `ag-kit mcp serve`"};
  return{...result,file:path.relative(target,result.file)};
}
