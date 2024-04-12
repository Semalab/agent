#!/usr/bin/env node

const { readFile, writeFile } = require('node:fs/promises');
const { parseArgs } = require('node:util');
const { JSHINT } = require('jshint');
const { Linter } = require('eslint');

const JSHINT_OPTIONS = {
    "maxerr": 99999
};

function main(lines) {
    let eslint = [], jshint = [], es = 5;

    let jshint_options = Object.assign({}, JSHINT_OPTIONS);

    // Run JSHint and see if the ECMA version needs to be upped
    JSHINT(lines, jshint_options);
    let data = JSHINT.data();
    if (data && data.errors) {
        jshint = data.errors;
        for (let m in jshint) {
            for (let i = 9; i--; i > 5) {
                if (jshint[m].reason.includes('ES' + i)) {
                    es = es > i ? es : i;
                    break;
                }
            }
        }
    }

    console.warn('ECMA version:', es);

    // Re-run JSHint if we saw an indication of a newer ECMA version
    if (es > 5) {
        jshint = [];
        jshint_options.esversion = es;
        JSHINT(lines, jshint_options);
        data = JSHINT.data();
        if (data && data.errors) jshint = data.errors;
    }

    // Run ESLint with the determined ECMA version
    let linter = new Linter();
    eslint = linter.verify(lines, { parserOptions: { ecmaVersion: es } });

    return { eslint, jshint };
}

(async () => {
    const options = {
        'output-file': {
            type: 'string',
            short: 'o'
        },
        'input-file': {
            type: 'string',
            short: 'i'
        }
    };
    const { values } = parseArgs({ options });

    try {
        const input_file = values['input-file'];
        const input = await readFile(input_file, { encoding: 'utf8' });

        let output = main(input);
        output.filename = input_file;
        output = JSON.stringify(output);

        const output_file = values['output-file'];
        if (output_file) {
            await writeFile(output_file, output + '\n');
        } else {
            console.log(output);
        }
    } catch (e) {
        console.error(e);
        process.exit(1);
    }
})();
