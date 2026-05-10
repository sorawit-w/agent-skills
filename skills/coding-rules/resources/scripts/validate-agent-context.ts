// coding-rules/scripts/validate-agent-context.ts
//
// Validates `agent-context.yaml` (at project root) against the
// `agent-context.schema.yaml` bundled inside this coding-rules install.
//
// Usage (from repo root) — pick whichever path matches your install:
//   bun run .ai/coding-rules/resources/scripts/validate-agent-context.ts
//   bun run <plugin-install>/skills/coding-rules/resources/scripts/validate-agent-context.ts
//
// Requirements:
//   pnpm add -D ajv ajv-formats js-yaml
//   or
//   bun add -d ajv ajv-formats js-yaml

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import yaml from "js-yaml";
import Ajv from "ajv";
import addFormats from "ajv-formats";

// Schema lives next to this script's parent (coding-rules root), regardless of where
// the user installed coding-rules. Data lives at the project root.
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const SCHEMA_PATH = path.resolve(SCRIPT_DIR, "..", "agent-context.schema.yaml");
const CONTEXT_PATH = path.resolve(process.cwd(), "agent-context.yaml");

function readYaml(filePath: string) {
  if (!fs.existsSync(filePath)) {
    console.error(`❌ File not found: ${filePath}`);
    process.exit(1);
  }

  try {
    const raw = fs.readFileSync(filePath, "utf8");
    const data = yaml.load(raw);
    if (data === null || typeof data !== "object") {
      console.error(`❌ Invalid or empty YAML in: ${filePath}`);
      process.exit(1);
    }
    return data;
  } catch (err) {
    console.error(`❌ Failed to read/parse YAML: ${filePath}`);
    console.error(err);
    process.exit(1);
  }
}

function main() {
  console.log("🔍 Validating `agent-context.yaml` against `agent-context.schema.yaml`...");

  const schema = readYaml(SCHEMA_PATH);
  const context = readYaml(CONTEXT_PATH);

  const ajv = new Ajv({
    allErrors: true,
    strict: false, // keep this relaxed; the schema is for structure, not pain
  });
  addFormats(ajv);

  const validate = ajv.compile(schema);
  const valid = validate(context);

  if (!valid) {
    console.error("❌ agent-context.yaml is NOT valid:");
    if (validate.errors && validate.errors.length) {
      for (const err of validate.errors) {
        console.error(
          `  - ${err.instancePath || "/"} ${err.message}${
            err.params ? ` (${JSON.stringify(err.params)})` : ""
          }`
        );
      }
    }
    process.exit(1);
  }

  console.log("✅ agent-context.yaml is valid and schema-compliant.");
  process.exit(0);
}

main();
