import React, { FormEvent } from 'react';

// Import types
import { CellFocusedEvent } from 'ag-grid-community';
import { SheetJSON, ErrorJSON } from '../widget';

// Import sheet and code components
import MitoSheet from './MitoSheet';
import SheetTab from './SheetTab';
import FormulaBar from './FormulaBar';
import MitoToolbar from './MitoToolbar';
import DocumentationSidebar from './DocumentationSidebar';

// Import modals
import ErrorModal from './ErrorModal';
import ExportModal from './ExportModal';
import RepeatAnalysisModal from './RepeatAnalysisModal';

// Import css
import "../../css/mito.css"

export interface ColumnSpreadsheetCodeJSON {
    [Key: string]: string;
}

type MitoProps = {
    dfName: string;
    columnSpreadsheetCodeJSON: ColumnSpreadsheetCodeJSON;
    sheetJSON: SheetJSON;
    send: (msg: Record<string, unknown>) => void
    model_id: string;
};

type MitoState = {
    dfName: string;
    columnSpreadsheetCodeJSON: ColumnSpreadsheetCodeJSON;
    sheetJSON: SheetJSON;
    formulaBarValue: string;
    selectedColumn: string;
    selectedRowIndex: number;
    errorJSON: ErrorJSON;
    editingCellColumn : string;
    editingCellRowIndex : number;
    documentationOpen: boolean;
    modal: ModalEnum;
};

const INDEX_COLUMN = "index";


export enum ModalEnum {
    None = 'None',
    Error = 'Error',
    RepeatAnalysis = 'RepeatAnalysis',
    Export = 'Export'
}


class Mito extends React.Component<MitoProps, MitoState> {

    constructor(props: MitoProps) {
        super(props);

        this.state = {
            columnSpreadsheetCodeJSON: this.props.columnSpreadsheetCodeJSON,
            dfName: this.props.dfName,
            sheetJSON: this.props.sheetJSON,
            formulaBarValue: this.props.sheetJSON.data[0][0],
            selectedColumn: this.props.sheetJSON.columns[0].toString(),
            selectedRowIndex: 0,
            /*
                note that editingCellColumn and editingCellRowIndex should both either
                be set to these default values or they should be set to valid cell values
            */
            editingCellColumn: "",
            editingCellRowIndex: -1,
            documentationOpen: false,
            modal: ModalEnum.None,
            errorJSON: {
                event: '',
                type: '',
                header: '',
                to_fix: ''
            }
        };

        this.cellFocused = this.cellFocused.bind(this);
        this.handleFormulaBarEdit = this.handleFormulaBarEdit.bind(this);
        this.handleFormulaBarSubmit = this.handleFormulaBarSubmit.bind(this);
        this.sendCellValueUpdate = this.sendCellValueUpdate.bind(this);
        this.setEditingMode = this.setEditingMode.bind(this);
        this.setDocumentation = this.setDocumentation.bind(this);
        this.setModal = this.setModal.bind(this);
        this.getCurrentModalComponent = this.getCurrentModalComponent.bind(this);
    }

    /* 
        This function is responsible for turning cell editing mode on and off
        by setting the state of: 
            1. editingMode
            2. editingCellColumn
            3. editingCellRowIndex
        This function is called by MitoCellEditor's constructor. 

    */
    setEditingMode(on: boolean, column: string, rowIndex: number) : void {
        if (on && this.state.editingCellRowIndex === -1) {
            /* 
                if this function is turning on cell editing mode (on === true), while 
                we're not already in cell editing mode (editingCellRowIndex === -1), then save the cell editor's 
                cell. This gets called when the user double clicks on a cell on presses enter 
                while a cell is selected and we're not in cell editing mode. 
            */
            this.setState({
                editingCellColumn: column,
                editingCellRowIndex: rowIndex
            });
        } else if (on && this.state.editingCellRowIndex !== -1) {
            /*
                trying to turn cell editing mode on while cell editing mode is already on
                occurs after the CellFocused function call startEditingCell, causing the cell editor
                to be re-constructed and thus call this function again. 
            */ 
            return;
        } else {
            /* 
                turn off cell editing mode -- this can occur for a number of reasons. 
                See: https://www.ag-grid.com/javascript-grid-cell-editing/#stop-end-editing
                However, we don't allow the user to exit cell editing mode via a new Cell Focus Event
            */
            this.setState({
                editingCellColumn: "",
                editingCellRowIndex: -1
            });
        }
    }

    /* 
        We handle this event differently depending on whether we're in or out of cell editing mode
    */
    cellFocused(event : CellFocusedEvent) : void {
        const column = event.column.getColId();

        if (this.state.editingCellRowIndex !== -1) {
            /* 
                If we're in editing mode,turn editing back on for the currently edited cell
                This is technically a bit of a hacky solution to pass in the charPress as the selected column 
            */
            const selectedColumn = JSON.stringify({selectedColumn:column})

            /*  
                turn on the correct cell editor. see extensive comment in MitoCellEditor.tsx 
                constructor about hacking CharPress
            */
            const editingModeParams = {
                rowIndex: this.state.editingCellRowIndex,
                colKey: this.state.editingCellColumn,
                charPress: selectedColumn
            }

            // turn the editing cell's cell editor back on!
            window.gridApiMap?.get(this.props.model_id)?.startEditingCell(editingModeParams);
        } else {
            // if we're not in editing mode, get the formula for the formula bar

            // if the column is the index column, then we reset the selected cell state
            if (column === INDEX_COLUMN) {
                this.setState({
                    selectedColumn: '',
                    selectedRowIndex: 0,
                    formulaBarValue: ''
                });
                return;
            }

            // otherwise, get the cell's formula to display
            const columnIndex = this.state.sheetJSON.columns.indexOf(column);
            const rowIndex = event.rowIndex;

            const columnFormula = this.state.columnSpreadsheetCodeJSON[column];
            let formulaBarValue = '';
            if (columnFormula !== '') {
                // if the cell has a formula, display it in the formula bar
                formulaBarValue = columnFormula

            } else {
                // otherwise display the value in the formula bar
                formulaBarValue = this.state.sheetJSON.data[rowIndex][columnIndex];
            }
            
            this.setState({
                selectedColumn: column,
                selectedRowIndex: rowIndex,
                formulaBarValue: formulaBarValue
            });
        }
    }

    handleFormulaBarEdit(e: FormEvent<HTMLInputElement>) : void {
        this.setState({
            formulaBarValue: e.currentTarget.value
        });
    }

    // TODO: do we want a different type of edit for a value change and a formula change or will 
    // we just detect that in the backend and apply the correct edit rules?
    handleFormulaBarSubmit(e : React.FormEvent<HTMLFormElement>) : void {
        e.preventDefault();
        this.sendCellValueUpdate(this.state.selectedColumn, this.state.formulaBarValue);
    }

    // TODO: this event should be broken out into a formula edit and a value edit
    sendCellValueUpdate(column : string, newValue : string) : void {
        /*
            We don't send the formula to the evaluator while in cell editing mode
            because this function gets called after the CellValueChangedEvent fires 
            each time the cell editor is closed. 
            
            However, the cell editor closes each time the user uses their mouse 
            to reference another column - which isn't a finished update yet!
        */
        if (this.state.editingCellRowIndex === -1) {
            this.props.send({
                'event': 'edit_event',
                'type': 'cell_edit',
                'id': '123',
                'timestamp': '456',
                'address': column,
                'new_formula': newValue
            });
        }
    }

    setDocumentation(documentationOpen: boolean) : void {
        this.setState({documentationOpen: documentationOpen});
    }

    getCurrentModalComponent(): JSX.Element {
        // Returns the JSX.element that is currently, open, and is used
        // in render to display this modal
        switch(this.state.modal) {
            case ModalEnum.None: return <div></div>;
            case ModalEnum.Error: return (
                <ErrorModal
                    errorJSON={this.state.errorJSON}
                    setModal={this.setModal}
                    />
            )
            case ModalEnum.RepeatAnalysis: return (
                <RepeatAnalysisModal
                    setModal={this.setModal}
                    />
            )
            case ModalEnum.Export: return (
                <ExportModal
                    setModal={this.setModal}
                    />
            )
        }
    }

    setModal(modal: ModalEnum) : void {
        this.setState({
            'modal': modal
        });
    }

    // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
    render() {
        // set the selected cell for the cell indicator in the mito toolbar
        const selectedCell = this.state.selectedColumn + (this.state.selectedRowIndex + 1).toString()
                            
        return (
            <div className="mito-container">
                <div className="mitosheet">
                    <MitoToolbar 
                        sheetJSON={this.state.sheetJSON} 
                        selectedCell={selectedCell} 
                        send={this.props.send}
                        setDocumentation={this.setDocumentation}
                        setModal={this.setModal}
                        model_id={this.props.model_id}
                        />
                    <FormulaBar
                        formulaBarValue={this.state.formulaBarValue}
                        handleFormulaBarEdit={this.handleFormulaBarEdit}
                        handleFormulaBarSubmit={this.handleFormulaBarSubmit} 
                    />
                    <MitoSheet 
                        sheetJSON={this.state.sheetJSON} 
                        setEditingMode={this.setEditingMode}
                        cellFocused={this.cellFocused}
                        send={this.props.send}
                        model_id={this.props.model_id}
                        sendCellValueUpdate={this.sendCellValueUpdate} 
                        />
                    <div key={this.state.dfName} className="sheet-tab-bar">
                        <SheetTab sheetName={this.state.dfName}></SheetTab>
                    </div>
                </div>
                {this.getCurrentModalComponent()}
                {this.state.documentationOpen && 
                    <div className="sidebar">
                        <DocumentationSidebar setDocumentation={this.setDocumentation}/>
                    </div>
                }                
            </div>
        );
    }

}


export default Mito;