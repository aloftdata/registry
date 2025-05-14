// Load Flat Data
import { readJSON, writeJSON } from 'https://deno.land/x/flat@0.0.15/mod.ts'

// Read downloaded_filename (aloft_datasets.json)
const input_file = 'aloft_datasets.json' // Or Deno.args[0]
const json = await readJSON(input_file)

// Select datasets (in json.hits.hits)
const datasets = json.hits.hits
console.log(json)

// Write JSON
const output_file = 'aloft_datasets.json'
await writeJSON(output_file, datasets, null, 2) // 2: pretty print with 2 spaces
console.log("Wrote a processed file")
