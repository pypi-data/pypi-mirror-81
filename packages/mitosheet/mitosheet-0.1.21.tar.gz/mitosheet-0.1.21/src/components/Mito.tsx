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
import RepeatAnalysisModal from './RepeatAnalysisModal';

// Import css
import "../../css/mito.css"

interface ColumnSpreadsheetCodeJSON {
    [Key: string]: string;
}


type MitoProps = {
    dfName: string;
    columnSpreadsheetCodeJSON: ColumnSpreadsheetCodeJSON;
    sheetJSON: SheetJSON;
    send: any
};

type MitoState = {
    dfName: string;
    columnSpreadsheetCodeJSON: ColumnSpreadsheetCodeJSON;
    sheetJSON: SheetJSON;
    formulaBarValue: string;
    selectedColumn: string;
    selectedRowIndex: number;
    documentationOpen: boolean;
    modal: ModalEnum;
    errorJSON: ErrorJSON;
};

export enum ModalEnum {
    None = "None",
    Error = "Error",
    RepeatAnalysis = "RepeatAnalysis"
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
        this.setDocumentation = this.setDocumentation.bind(this);
        this.setModal = this.setModal.bind(this);
        this.getCurrentModalComponent = this.getCurrentModalComponent.bind(this);
    }

    cellFocused(event : CellFocusedEvent) {
        const column = event.column.getColId();
        const columnIndex = this.state.sheetJSON.columns.indexOf(column);
        const rowIndex = event.rowIndex;

        if (column === 'index') {
            // if the index column is selected, clear the formula bar
            this.setState({
                selectedColumn: "index",
                selectedRowIndex: rowIndex,
                formulaBarValue: ""
            });
        } else {
            // if a non-index column is selected, get the formula
            const columnFormula = this.state.columnSpreadsheetCodeJSON[column];
            let formulaBarValue = '';
            if (columnFormula !== '') {
                // if the cell has a formula, then display the formula
                formulaBarValue = columnFormula

            } else {
                // if the cell does not have a formula, display the value
                formulaBarValue = this.state.sheetJSON.data[rowIndex][columnIndex];
            }

            // update state
            this.setState({
                selectedColumn: column,
                selectedRowIndex: rowIndex,
                formulaBarValue: formulaBarValue
            });
        }
    }

    handleFormulaBarEdit(e: FormEvent<HTMLInputElement>) {
        this.setState({
            formulaBarValue: e.currentTarget.value
        });
    }

    // TODO: do we want a different type of edit for a value change and a formula change or will 
    // we just detect that in the backend and apply the correct edit rules?
    handleFormulaBarSubmit(e : React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        this.sendCellValueUpdate(this.state.selectedColumn, this.state.formulaBarValue);
    }

    // TODO: this event should be broken out into a formula edit and a value edit
    sendCellValueUpdate(column : string, newValue : string) {
        this.props.send({
            'event': 'edit_event',
            'type': 'cell_edit',
            'id': '123',
            'timestamp': '456',
            'address': column,
            'new_formula': newValue
        });
    }

    setDocumentation(documentationOpen: boolean) {
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
        }
    }

    setModal(modal: ModalEnum) {
        this.setState({
            'modal': modal
        });
    }

    render() {
        // set the selected cell for the cell indicator in the mito toolbar
        let selectedCell = this.state.selectedColumn + (this.state.selectedRowIndex + 1).toString()
                            
        return (
            <div className="mito-container">
                <div className="mitosheet">
                    <MitoToolbar 
                        sheetJSON={this.state.sheetJSON} 
                        selectedCell={selectedCell} 
                        send={this.props.send}
                        setDocumentation={this.setDocumentation}
                        setModal={this.setModal}
                        />
                    <FormulaBar
                        formulaBarValue={this.state.formulaBarValue}
                        handleFormulaBarEdit={this.handleFormulaBarEdit}
                        handleFormulaBarSubmit={this.handleFormulaBarSubmit} 
                    />
                    <MitoSheet 
                        sheetJSON={this.state.sheetJSON} 
                        cellFocused={this.cellFocused}
                        send={this.props.send}
                        sendCellValueUpdate={this.sendCellValueUpdate} />
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