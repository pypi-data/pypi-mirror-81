// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Component } from 'react';
import { ICellEditorParams } from 'ag-grid-community';
import { functionDocumentationObjects, FunctionDocumentationObject } from './DocumentationSidebar';

import DocumentationBox from './editor/DocumentationBox';

type CellEditorState = {
    value: string | number,
    input: HTMLInputElement | null
};

type CellEditorProps = ICellEditorParams & {
    setEditingMode : (on: boolean, column: string, rowIndex: number) => void
    columnSelected : string
}

const keyboardKeys = {
  ENTER_KEY: "Enter",
  TAB_KEY: "Tab",
  ESCAPE_KEY: "Escape"
} 

export default class MitoCellEditor extends Component<CellEditorProps, CellEditorState> {
  constructor(props : CellEditorProps) {
    super(props);

    // Set the cell's value
    if (props.charPress != null) {

      /* 
      We hack the charPress param. The charPress param is usually used to tell the cell editor
      which character was pressed to enter cell editing mode. However, we use also use it to pass
      the column that the user selected with their mouse. If charPress is not null then either:
        1. the user was in cell editing mode and clicked on a column with their mouse. Then charPress 
           is a stringified JSON object of the form: 
           {
              "selectedColumn": column
           }
           where column is the columnID of the column the user selected with their mouse. This columnID
           should be appended to the cell editor value to be included in the formula. 

        2. the user entered cell editing mode by pressing a key instead of Enter or double clicking. In this case,
           the current cell value should be overwritten by charPress 
      */

      if (props.charPress.length > 1) {
        // if a column was passed, append it to the cell's value
        const selectedColumn = JSON.parse(props.charPress).selectedColumn
        this.state = {
          value: props.value + selectedColumn,
          input: null
        }
      } else {
        // if a character was passed, overwrite the cell's value
        // TODO: update the spec with this behavior
        this.state = {
          value: props.charPress,
          input: null
        }
      }
    } else {
      // otherwise keep the original value
      this.state = {
        value: props.value,
        input: null
      }
    }
    
    // turn on cell editing mode
    const column = props.colDef.field ? props.colDef.field : "";
    props.setEditingMode(true, column, props.rowIndex);

    /* turn off cell editing mode when ENTER or Tab is pressed  */
    document.addEventListener("keydown", (event) => {
      if (
        event.key === keyboardKeys.ENTER_KEY || 
        event.key === keyboardKeys.TAB_KEY ||
        event.key === keyboardKeys.ESCAPE_KEY
        ) {
        props.setEditingMode(false, "", -1);
      }
    });

    this.getValue = this.getValue.bind(this);
    this.isPopup = this.isPopup.bind(this);
    this.handleOnChange = this.handleOnChange.bind(this);
    this.afterGuiAttached = this.afterGuiAttached.bind(this);
  }

  getValue() : string | number {
    return this.state.value;
  }

  /* Make the cell editor a popup, so we can display suggestion/documentation box */ 
  isPopup() : boolean {
    return true;
  }

  /* update the cell value while typing */
  handleOnChange (event : React.ChangeEvent<HTMLInputElement>) : void {
    this.setState({
      value: event.target.value
    });
  }

  /*
    This function is called by ag-grid after this component
    is rendered; we simply focus on the input feild rendered
    below so the user can begin typing immediately!
  */
  afterGuiAttached() : void {
    this.state.input?.focus();
  }

  /*
    This function returns the current function that should
    be displayed in the documentation box, based on if the
    documentation box open condition is met. 

    If the documentation box open condition is not met, this 
    returns undefined. 
  */
  getDocumentationBoxFunction() : FunctionDocumentationObject | undefined {
    // Finds all instances of functions that are not followed by a closing paren
    // e.g. all functions that are still being edited.
    const docBoxRe = /[A-Z]+\((?![^)]*\))/g;

    if (typeof this.state.value == 'string') {
      const functionMatches = this.state.value?.match(docBoxRe);
      if (!functionMatches) {
        return undefined;
      }
      // We take the _last_ function that has been written, as this is the funciton
      // being edited currently.
      const lastFunction = functionMatches[functionMatches.length - 1];
      // Strip off the last ( from the function name
      const lastFunctionClean = lastFunction.substr(0, lastFunction.length - 1);

      return functionDocumentationObjects.find((funcDocObject) => {
        return funcDocObject.function === lastFunctionClean;
      });
    }
    return undefined;
  }

  

  
  render() : JSX.Element {
    const documentationBoxFunction = this.getDocumentationBoxFunction();

    return (
      <div>
        <input 
          ref={(input) => {if (!this.state.input) {this.setState({input: input})}}}
          className="ag-cell-auto-height ag-cell-inline-editing"
          name="value" 
          value={this.state.value} 
          onChange={this.handleOnChange} 
          tabIndex={1}/>
        {
          documentationBoxFunction &&
          <DocumentationBox
            funcDocObject={documentationBoxFunction}
            />
        }
      </div>
    );
  }
}