#!/usr/bin/env bash

# Basic Audio Transcription Example
# Demonstrates how to use the audio-transcriber skill manually

set -euo pipefail

# Configuration
AUDIO_FILE="${1:-}"
MODEL="${MODEL:-base}"  # Options: tiny, base, small, medium, large
OUTPUT_FORMAT="${OUTPUT_FORMAT:-markdown}"  # Options: markdown, txt, srt, vtt, json

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
error() {
    echo -e "${RED}❌ Error: $1${NC}" >&2
    exit 1
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if audio file is provided
if [[ -z "$AUDIO_FILE" ]]; then
    error "Usage: $0 <audio_file>"
fi

# Verify file exists
if [[ ! -f "$AUDIO_FILE" ]]; then
    error "File not found: $AUDIO_FILE"
fi

# Step 0: Discovery - Check for transcription tools
info "Step 0: Discovering transcription tools..."

TRANSCRIBER=""
if python3 -c "import faster_whisper" 2>/dev/null; then
    TRANSCRIBER="faster-whisper"
    success "Faster-Whisper detected (optimized)"
elif python3 -c "import whisper" 2>/dev/null; then
    TRANSCRIBER="whisper"
    success "OpenAI Whisper detected"
else
    error "No transcription tool found. Install with: pip install faster-whisper"
fi

# Check for ffmpeg
if command -v ffmpeg &>/dev/null; then
    success "ffmpeg available (format conversion enabled)"
else
    warn "ffmpeg not found (limited format support)"
fi

# Step 1: Extract metadata
info "Step 1: Extracting audio metadata..."

FILE_SIZE=$(du -h "$AUDIO_FILE" | cut -f1)
info "File size: $FILE_SIZE"

# Get duration if ffprobe is available
if command -v ffprobe &>/dev/null; then
    DURATION=$(ffprobe -v error -show_entries format=duration \
        -of default=noprint_wrappers=1:nokey=1 "$AUDIO_FILE" 2>/dev/null || echo "0")
    
    # Convert to HH:MM:SS
    if command -v date &>/dev/null; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            DURATION_HMS=$(date -u -r "${DURATION%.*}" +%H:%M:%S 2>/dev/null || echo "Unknown")
        else
            # Linux
            DURATION_HMS=$(date -u -d @"${DURATION%.*}" +%H:%M:%S 2>/dev/null || echo "Unknown")
        fi
    else
        DURATION_HMS="Unknown"
    fi
    
    info "Duration: $DURATION_HMS"
else
    warn "ffprobe not found - cannot extract duration"
    DURATION="0"
    DURATION_HMS="Unknown"
fi

# Check file size warning
SIZE_MB=$(du -m "$AUDIO_FILE" | cut -f1)
if [[ $SIZE_MB -gt 25 ]]; then
    warn "Large file ($FILE_SIZE) - processing may take several minutes"
    read -p "Continue? [Y/n]: " CONTINUE
    if [[ "$CONTINUE" =~ ^[Nn] ]]; then
        info "Transcription cancelled"
        exit 0
    fi
fi

# Step 2: Transcribe using Python
info "Step 2: Transcribing audio..."

OUTPUT_FILE="${AUDIO_FILE%.*}.md"
TEMP_JSON="/tmp/transcription_$$.json"

python3 << EOF
import sys
import json
from datetime import datetime

try:
    if "$TRANSCRIBER" == "faster-whisper":
        from faster_whisper import WhisperModel
        model = WhisperModel("$MODEL", device="cpu", compute_type="int8")
        segments, info = model.transcribe("$AUDIO_FILE", language=None, vad_filter=True)
        
        data = {
            "language": info.language,
            "language_probability": round(info.language_probability, 2),
            "duration": info.duration,
            "segments": []
        }
        
        for segment in segments:
            data["segments"].append({
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment.text.strip()
            })
    else:
        import whisper
        model = whisper.load_model("$MODEL")
        result = model.transcribe("$AUDIO_FILE")
        
        data = {
            "language": result["language"],
            "duration": result["segments"][-1]["end"] if result["segments"] else 0,
            "segments": result["segments"]
        }
    
    with open("$TEMP_JSON", "w") as f:
        json.dump(data, f)
    
    print(f"✅ Language detected: {data['language']}")
    print(f"📝 Transcribed {len(data['segments'])} segments")
    
except Exception as e:
    print(f"❌ Error: {e}", file=sys.stderr)
    sys.exit(1)
EOF

# Check if transcription succeeded
if [[ ! -f "$TEMP_JSON" ]]; then
    error "Transcription failed"
fi

# Step 3: Generate Markdown output
info "Step 3: Generating Markdown report..."

python3 << 'EOF'
import json
import sys
from datetime import datetime

# Load transcription data
with open("${TEMP_JSON}") as f:
    data = json.load(f)

# Prepare metadata
filename = "${AUDIO_FILE}".split("/")[-1]
file_size = "${FILE_SIZE}"
duration_hms = "${DURATION_HMS}"
language = data["language"]
process_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
num_segments = len(data["segments"])

# Generate Markdown
markdown = f"""# Audio Transcription Report

## 📊 Metadata

| Field | Value |
|-------|-------|
| **File Name** | {filename} |
| **File Size** | {file_size} |
| **Duration** | {duration_hms} |
| **Language** | {language.upper()} |
| **Processed Date** | {process_date} |
| **Segments** | {num_segments} |
| **Transcription Engine** | ${TRANSCRIBER} (model: ${MODEL}) |

---

## 🎙️ Full Transcription

"""

# Add transcription with timestamps
for seg in data["segments"]:
    start_time = f"{int(seg['start'] // 60):02d}:{int(seg['start'] % 60):02d}"
    end_time = f"{int(seg['end'] // 60):02d}:{int(seg['end'] % 60):02d}"
    markdown += f"**[{start_time} → {end_time}]**  \n{seg['text']}\n\n"

markdown += """---

## 📝 Summary

*Automatic summary generation requires AI integration (Claude/GPT).*  
*For now, review the full transcription above.*

---

*Generated by audio-transcriber skill example script*  
*Transcription engine: ${TRANSCRIBER} | Model: ${MODEL}*
"""

# Write to file
with open("${OUTPUT_FILE}", "w") as f:
    f.write(markdown)

print(f"✅ Markdown report saved: ${OUTPUT_FILE}")
EOF

# Clean up
rm -f "$TEMP_JSON"

# Step 4: Display summary
success "Transcription complete!"
echo ""
echo "📊 Results:"
echo "  Output file: $OUTPUT_FILE"
echo "  Transcription engine: $TRANSCRIBER"
echo "  Model: $MODEL"
echo ""
info "Next steps:"
echo "  1. Review the transcription: cat $OUTPUT_FILE"
echo "  2. Edit if needed: vim $OUTPUT_FILE"
echo "  3. Share with team or archive"
EOF
