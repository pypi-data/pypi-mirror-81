import React from 'react';

import '../../css/function-documentation.css';
import '../../css/margins.css';

import { FunctionDocumentationObject } from './DocumentationSidebar';

/*
    Returns a sidebar that contains the documentation for a single function. 
*/
const FunctionDocumentation = 
    (props: {
        funcDocObject: FunctionDocumentationObject;
        setSelectedFunction: (functionName: string) => void;
        setDocumentation: (documentationOpen: boolean) => void;
    }): JSX.Element => {
    return (
        <div>
            <div className='function-documentation-header'>
                <div className='function-documentation-header-back' onClick={() => {props.setSelectedFunction('')}}>
                    <svg width="7" height="11" viewBox="0 0 7 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M0 5.5L6.75 0.73686L6.75 10.2631L0 5.5Z" fill="black"/>
                    </svg>
                </div>
                <div className='function-documentation-header-text'>
                    {props.funcDocObject.function} Documentation
                </div>
                <div className='function-documentation-header-close' onClick={() => {props.setDocumentation(false)}}>
                    X
                </div>
            </div>
            <div className='function-documentation'>
                <h1 className='function-documentation-function-name'>
                    {props.funcDocObject.function}
                </h1>
                <p>
                    {props.funcDocObject.description}
                </p>
                <h2 className='mb-0'>
                    Examples
                </h2>
                <ul className='function-documentation-example-list blue-text'>
                    {props.funcDocObject.examples?.map((example) => {
                        return <li className='function-documentation-example' key={example}>{example}</li>
                    })}
                </ul>
                <h2 className='mb-0'>
                    Syntax
                </h2>
                <p className='blue-text'>
                    {props.funcDocObject.syntax}
                </p>
                <ul>
                    {props.funcDocObject.syntax_elements?.map((syntax_element) => {
                        return (
                            <li key={syntax_element.element}>
                                <p className='blue-text'>{syntax_element.element}</p>
                                {syntax_element.description}
                            </li>
                        )
                    })}
                </ul>
            </div>
        </div>
    );    
};

export default FunctionDocumentation;