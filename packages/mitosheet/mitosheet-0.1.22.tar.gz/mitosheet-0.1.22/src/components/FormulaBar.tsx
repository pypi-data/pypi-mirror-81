import React, { FormEvent } from 'react';

// Import css
import "../../css/formula-bar.css";

const FormulaBar = (props: {
    formulaBarValue: string, 
    handleFormulaBarEdit: (e: FormEvent<HTMLInputElement>) => void,
    handleFormulaBarSubmit: (e : FormEvent<HTMLFormElement>) => void
}): JSX.Element => {

    return(
        <div className="vertical-align-content formula-bar-container">
            <div className="formula-bar">
                <p className="fx-text">Fx</p>
                <div className="vertical-line"></div>
                <form onSubmit={props.handleFormulaBarSubmit}>
                    <input 
                        className="formula-bar-input"
                        value={props.formulaBarValue} 
                        onChange={(e) => props.handleFormulaBarEdit(e)}
                        />
                </form>
            </div>
        </div>
    )
}

export default FormulaBar
