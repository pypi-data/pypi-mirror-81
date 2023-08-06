// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Component } from 'react';
import { ICellEditorParams } from 'ag-grid-community';
import { functionDocumentationObjects, FunctionDocumentationObject } from './DocumentationSidebar';

import DocumentationBox from './editor/DocumentationBox';
import SuggestionBox from './editor/SuggestionBox';


type CellEditorState = {
    value: string | number,
    input: HTMLInputElement | null,
    suggestionIndex: number
};

type CellEditorProps = ICellEditorParams & {
    setEditingMode : (on: boolean, column: string, rowIndex: number) => void
    columnSelected : string
}

const keyboardKeys = {
  ENTER_KEY: "Enter",
  TAB_KEY: "Tab",
  ESCAPE_KEY: "Escape",
  UP: 'ArrowUp',
  DOWN: 'ArrowDown',
  LEFT: 'ArrowLeft',
  RIGHT: 'ArrowRight',
  // These events have IE/Edge differences
  IE_UP: 'Up',
  IE_DOWN: 'Down',
  IE_LEFT: 'Left',
  IE_RIGHT: 'Right'
}

export const TAKE_SUGGESTION_KEYS = [keyboardKeys.ENTER_KEY, keyboardKeys.TAB_KEY];
const CLOSE_INPUT_KEYS = [keyboardKeys.ENTER_KEY, keyboardKeys.TAB_KEY, keyboardKeys.ESCAPE_KEY];
export const ARROW_UP_KEYS = [keyboardKeys.UP, keyboardKeys.IE_UP];
export const ARROW_DOWN_KEYS = [keyboardKeys.DOWN, keyboardKeys.IE_DOWN];


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
          input: null,
          suggestionIndex: 0
        }
      } else {
        // if a character was passed, overwrite the cell's value
        // TODO: update the spec with this behavior
        this.state = {
          value: props.charPress,
          input: null,
          suggestionIndex: 0
        }
      }
    } else {
      // otherwise keep the original value
      this.state = {
        value: props.value,
        input: null,
        suggestionIndex: 0
      }
    }
    
    // turn on cell editing mode
    const column = props.colDef.field ? props.colDef.field : "";
    props.setEditingMode(true, column, props.rowIndex);

    this.getValue = this.getValue.bind(this);
    this.isPopup = this.isPopup.bind(this);
    this.handleOnChange = this.handleOnChange.bind(this);
    this.afterGuiAttached = this.afterGuiAttached.bind(this);
    this.getCurrentSuggestions = this.getCurrentSuggestions.bind(this);
    this.getDocumentationBoxFunction = this.getDocumentationBoxFunction.bind(this);
    this.onKeyDown = this.onKeyDown.bind(this);
    this.onMouseEnterSuggestion = this.onMouseEnterSuggestion.bind(this);
    this.selectSuggestion = this.selectSuggestion.bind(this);
    this.getAdjustedIndex = this.getAdjustedIndex.bind(this);
  }

  getValue() : string | number {
    return this.state.value;
  }

  /* Make the cell editor a popup, so we can display suggestion/documentation box */ 
  isPopup() : boolean {
    return true;
  }

  /* update the cell value while typing */
  handleOnChange(event : React.ChangeEvent<HTMLInputElement>) : void {
    this.setState({value: event.target.value});
  }

  /*
    This function is called by ag-grid after this component
    is rendered; we simply focus on the input feild rendered
    below so the user can begin typing immediately!

    Furthermore, we register the event handlers for this component.
  */
  afterGuiAttached() : void {
    this.state.input?.focus();
  }

  /*
    This function handles key presses on the cell editor input.

    If the suggestion box is open currently, than this function first checks 
    if this key press effects the suggestion box (e.g. scrolling or selecting a suggestion).

    Otherwise, we check if this event closes the cell editor.

    NOTE: we event.preventDefault() to stop events from having unintended
    consequences if they cause effects we handle ourselves. For example, this
    prevents TAB from selecting the next form field.

    NOTE: the events handled by this functions should correspond to the events 
    suppressed in editing mode in the ag-grid, to avoid unintended behavior
  */
  onKeyDown(event: React.KeyboardEvent<HTMLInputElement>) : void {
    const suggestions = this.getCurrentSuggestions();
    if (suggestions !== undefined) {
      if (TAKE_SUGGESTION_KEYS.includes(event.key)) {
        event.preventDefault();
        // We mod below just as one last safety check for an out of bound index, which we
        // also ensure with the getAdjustedIndex function
        const selectedFunctionObj = suggestions.suggestions[this.state.suggestionIndex % suggestions.suggestions.length];
        const restOfFunction = selectedFunctionObj.function.substring(suggestions.match.length);
        return this.selectSuggestion(restOfFunction);
      } else if (ARROW_UP_KEYS.includes(event.key)) {
        event.preventDefault();
        return this.setState((prevState) => {
          return {suggestionIndex: this.getAdjustedIndex(prevState.suggestionIndex - 1, suggestions)};
        });
      } else if (ARROW_DOWN_KEYS.includes(event.key)) {
        event.preventDefault();
        return this.setState((prevState) => {
          return {suggestionIndex: this.getAdjustedIndex(prevState.suggestionIndex + 1, suggestions)};
        });
      } 
    }
    
    // NOTE: we should always check the close events _last_, in case the keypresses
    // were trying to do other things!
    if (CLOSE_INPUT_KEYS.includes(event.key)) {
      event.preventDefault();
      this.props.setEditingMode(
        false, 
        this.props.column.getColId(), 
        this.props.rowIndex
      );
    }
  }

  /*
    This function returns the current suggestions, which are any
    functions who are prepended by the current ending string, which
    must be all capital alphabetic characters.
  */
  getCurrentSuggestions() : {match: string; suggestions: Array<FunctionDocumentationObject>} | undefined {
    const suggestionBoxRe = /[A-Z]+/g;

    if (typeof this.state.value == 'string') {
      const functionMatches = this.state.value?.match(suggestionBoxRe);
      if (!functionMatches) {
        return undefined;
      }
      const lastMatch = functionMatches[functionMatches.length - 1];
      if (this.state.value.endsWith(lastMatch)) {
        const suggestions = functionDocumentationObjects.filter((funcDocObject) => {
          return funcDocObject.function.startsWith(lastMatch);
        });
        if (suggestions.length > 0) {
          return {
            match: lastMatch,
            suggestions: suggestions
          }
        }
      }
    }
    return undefined;
  }

  /*
    Keeps the selected index for the suggestion box inbounds; the index
    should be the index of one of the suggestions!
  */
  getAdjustedIndex(
    index: number, 
    suggestions: {match: string; suggestions: Array<FunctionDocumentationObject>} 
  ) : number {

    // Fancy expression to keep it as a valid index
    return Math.min(Math.max(0, index), suggestions.suggestions.length - 1);
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
      const lastFunctionClean = lastFunction.substring(0, lastFunction.length - 1);

      return functionDocumentationObjects.find((funcDocObject) => {
        return funcDocObject.function === lastFunctionClean;
      });
    }
    return undefined;
  }

  // If you mouseover a suggestion, this selects it
  onMouseEnterSuggestion(suggestionIndex: number) : void {
    this.setState({suggestionIndex: suggestionIndex})
  }

  // Called when a suggestion is selected
  selectSuggestion(restOfFunction: string) : void {
    // We fill in the rest of the function, and reset the suggestion box
    this.setState((prevState) => {
      return {
        value: prevState.value + restOfFunction + '(',
        suggestionIndex: 0
      };
    }, () => {
      // We also refocus on the input feild
      this.state.input?.focus();
    });
  }
  
  render() : JSX.Element {
    const suggestions = this.getCurrentSuggestions();
    const documentationBoxFunction = this.getDocumentationBoxFunction();

    return (
      <div>
        <input 
          ref={(input) => {if (!this.state.input) {this.setState({input: input})}}}
          className="ag-cell-auto-height ag-cell-inline-editing"
          name="value" 
          value={this.state.value} 
          onChange={this.handleOnChange} 
          onKeyDown={this.onKeyDown}
          tabIndex={1}/>
        {
          suggestions !== undefined &&
          <SuggestionBox
            match={suggestions.match}
            suggestions={suggestions.suggestions}
            index={this.state.suggestionIndex}
            onMouseEnterSuggestion={this.onMouseEnterSuggestion}
            onSelectSuggestion={this.selectSuggestion}
            />
        }
        { /* Note: the suggestion box _always_ takes precendence over the documentation box */
          suggestions === undefined && documentationBoxFunction &&
          <DocumentationBox
            funcDocObject={documentationBoxFunction}
            />
        }
      </div>
    );
  }
}