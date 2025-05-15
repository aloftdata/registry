// Load Flat Data
import { readJSON, writeJSON } from 'https://deno.land/x/flat@0.0.15/mod.ts'

// Read downloaded_filename
const input_file = Deno.args[0]
const json = await readJSON(input_file)

// Select results (in json.hits.hits)
const results = json.hits.hits
console.log(results)

// Write JSON
const output_file = input_file.replace(".", "_processed.")
await writeJSON(output_file, results, null, 2) // 2: pretty print with 2 spaces
console.log("Wrote processed file")
