import React, { useState } from 'react';

import '../../css/documentation-sidebar.css';

import FunctionDocumentation from './FunctionDocumentation';

/* 
    To update this import, see the docs/README.md.

    NOTE: This import isn't working currently because of Webpack issues, 
    we're just in-lining the JSON for now!
*/
//import functionDocumentationObjects from '../data/function_documentation.json';
const functionDocumentationObjects: FunctionDocumentationObject[] = [{"function": "AVG", "description": "Returns the numerical mean value of the passed numbers and series.", "examples": ["AVG(1, 2)", "AVG(A, B)", "AVG(A, 2)"], "syntax": "AVG(value1, [value2, ...])", "syntax_elements": [{"element": "value1", "description": "The first number or series to consider when calculating the average."}, {"element": "value2, ... [OPTIONAL]", "description": "Additional numbers or series to consider when calculating the average."}]}, {"function": "CLEAN", "description": "Returns the text with the non-printable ASCII characters removed.", "examples": ["CLEAN('ABC\n')"], "syntax": "CLEAN(string)", "syntax_elements": [{"element": "string", "description": "The string or series whose non-printable characters are to be removed."}]}, {"function": "CONCATENATE", "description": "Returns the passed strings and series appended together.", "examples": ["CONCATENATE('Bite', 'the bullet')", "CONCATENATE(A, B)"], "syntax": "CONCATENATE(string1, [string2, ...])", "syntax_elements": [{"element": "string1", "description": "The first string or series."}, {"element": "string2, ... [OPTIONAL]", "description": "Additional strings or series to append in sequence."}]}, {"function": "FIND", "description": "Returns the position at which a string is first found within text, case-sensitive. Returns 0 if not found.", "examples": ["FIND(A, 'Jack')", "FIND('Ben has a friend Jack', 'Jack')"], "syntax": "FIND(text_to_search, search_for)", "syntax_elements": [{"element": "text_to_search", "description": "The text or series to search for the first occurrence of search_for."}, {"element": "search_for", "description": "The string to look for within text_to_search."}]}, {"function": "LEFT", "description": "Returns a substring from the beginning of a specified string.", "examples": ["LEFT(A, 2)", "LEFT('The first character!')"], "syntax": "LEFT(string, [number_of_characters])", "syntax_elements": [{"element": "string", "description": "The string or series from which the left portion will be returned."}, {"element": "number_of_characters [OPTIONAL, 1 by default]", "description": "The number of characters to return from the start of string."}]}, {"function": "LEN", "description": "Returns the length of a string.", "examples": ["LEN(A)", "LEN('This is 21 characters')"], "syntax": "LEN(string)", "syntax_elements": [{"element": "string", "description": "The string or series whose length will be returned."}]}, {"function": "LOWER", "description": "Converts a given string to lowercase.", "examples": ["=LOWER('ABC')", "=LOWER(A)", "=LOWER('Nate Rush')"], "syntax": "LOWER(string)", "syntax_elements": [{"element": "string", "description": "The string or series to convert to lowercase."}]}, {"function": "MID", "description": "Returns a segment of a string.", "examples": ["MID(A, 2, 2)", "MID('Some middle characters!', 3, 4)"], "syntax": "MID(string, starting_at, extract_length)", "syntax_elements": [{"element": "string", "description": "The string or series to extract the segment from."}, {"element": "starting_at", "description": "The index from the left of string from which to begin extracting."}, {"element": "extract_length", "description": "The length of the segment to extract."}]}, {"function": "MULTIPLY", "description": "Returns the product of two numbers.", "examples": ["MULTIPLY(2,3)", "MULTIPLY(A,3)"], "syntax": "MULTIPLY(factor1, [factor2, ...])", "syntax_elements": [{"element": "factor1", "description": "The first number to multiply."}, {"element": "factor2, ... [OPTIONAL]", "description": "Additional numbers or series to multiply."}]}, {"function": "PROPER", "description": "Capitalizes the first letter of each word in a specified string.", "examples": ["=PROPER('nate nush')", "=PROPER(A)"], "syntax": "PROPER(string)", "syntax_elements": [{"element": "string", "description": "The value or series to convert to convert to proper case."}]}, {"function": "RIGHT", "description": "Returns a substring from the beginning of a specified string.", "examples": ["RIGHT(A, 2)", "RIGHT('The last character!')"], "syntax": "RIGHT(string, [number_of_characters])", "syntax_elements": [{"element": "string", "description": "The string or series from which the right portion will be returned."}, {"element": "number_of_characters [OPTIONAL, 1 by default]", "description": "The number of characters to return from the end of string."}]}, {"function": "SUBSTITUTE", "description": "Replaces existing text with new text in a string.", "examples": ["SUBSTITUTE('Better great than never', 'great', 'late')", "SUBSTITUTE(A, 'dog', 'cat')"], "syntax": "SUBSTITUTE(text_to_search, search_for, replace_with, [occurrence_number])", "syntax_elements": [{"element": "text_to_search", "description": "The text within which to search and replace."}, {"element": "search_for", "description": " The string to search for within text_to_search."}, {"element": "replace_with", "description": "The string that will replace search_for."}, {"element": "occurrence_number", "description": "The number of times to perform the replace. Defaults to all."}]}, {"function": "SUM", "description": "Returns the sum of the given numbers and series.", "examples": ["SUM(10, 11)", "SUM(A, B, D, F)", "SUM(A, B, D, F)"], "syntax": "SUM(value1, [value2, ...])", "syntax_elements": [{"element": "value1", "description": "The first number or column to add together."}, {"element": "value2, ... [OPTIONAL]", "description": "Additional numbers or columns to sum."}]}, {"function": "TRIM", "description": "Returns a string with the leading and trailing whitespace removed.", "examples": ["=TRIM('  ABC', 'ABC')", "=TRIM('  ABC  ', 'ABC')", "=TRIM(' A B C ', 'A B C')"], "syntax": "TRIM(string)", "syntax_elements": [{"element": "string", "description": "The value or series to remove the leading and trailing whitespace from."}]}, {"function": "UPPER", "description": "Converts a given string to uppercase.", "examples": ["=UPPER('abc')", "=UPPER(A)", "=UPPER('Nate Rush')"], "syntax": "UPPER(string)", "syntax_elements": [{"element": "string", "description": "The string or series to convert to uppercase."}]}];

export interface FunctionDocumentationObject {
    function: string;
    description: string;
    examples?: (string)[] | null;
    syntax: string;
    syntax_elements?: (SyntaxElementsEntity)[] | null;
}

export interface SyntaxElementsEntity {
    element: string;
    description: string;
}

const DocumentationSidebar = (props: {setDocumentation: (documentationOpen: boolean) => void}): JSX.Element => {
    const [selectedFunction, setSelectedFunction] = useState('');

    const functionNameList = functionDocumentationObjects.map((funcDocObject) => {
        return (
            <li 
                className='documentation-sidebar-function-list-element'
                key={funcDocObject.function} 
                onClick={() => {setSelectedFunction(funcDocObject.function)}}>
                {funcDocObject.function}
            </li>
        )
    })

    // If there is a function selected, we just render the documentation page for the selected function
    if (selectedFunction !== '') {
        // Get the function object for this
        const funcDocObject = functionDocumentationObjects.find((funcDocObject) => {
            return funcDocObject.function === selectedFunction;
        })

        if (funcDocObject) {
            return (
                <FunctionDocumentation 
                    key={funcDocObject.function} 
                    funcDocObject={funcDocObject}
                    setSelectedFunction={setSelectedFunction}
                    setDocumentation={props.setDocumentation}
                    />
            )
        }
    } 

    // If no function is selected, we return a list of all the possible functions
    return (
        <div>
            <div className='function-documentation-header'>
                <div/> {/* Empty div spaces the function properly */}
                <div className='function-documentation-header-text'>
                    Documentation
                </div>
                <div className='function-documentation-header-close' onClick={() => {props.setDocumentation(false)}}>
                    X
                </div>
            </div>
            <div className='documentation-sidebar'>
                <h1 className='documentation-sidebar-function-title'>
                    Functions
                </h1>
                <ul className='documentation-sidebar-function-list'>
                    {functionNameList}
                </ul>
            </div>
        </div>
    ) 
};

export default DocumentationSidebar;