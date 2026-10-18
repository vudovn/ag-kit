import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

// True when the module at moduleUrl is the process entrypoint. Comparing file URLs built from
// the realpath keeps spaces, non-ASCII paths, Windows drive letters, and npm symlinks working.
export function isDirectRun(moduleUrl, argv1 = process.argv[1]) {
    if (!argv1) return false;
    try {
        return pathToFileURL(fs.realpathSync(path.resolve(argv1))).href === moduleUrl;
    } catch {
        return false;
    }
}
