//import React, { useState } from 'react';
import React from 'react';
import {AgGridReact} from 'ag-grid-react';
import { CellValueChangedEvent, CellFocusedEvent, GridReadyEvent } from 'ag-grid-community';
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';
import '../../css/mitosheet.css';
import MitoCellEditor from './MitoCellEditor';

// And functions for building components
import { buildGridData, buildGridColumns } from '../data-utils/gridData';

// Import types
import { SheetJSON } from '../widget';
    
const MitoSheet = (props: {
    sheetJSON: SheetJSON; 
    send: (msg: Record<string, unknown>) => void;
    sendCellValueUpdate: (column : string, newValue : string) => void; 
    setEditingMode: (on: boolean, column: string, rowIndex: number) => void;
    cellFocused: (event: CellFocusedEvent) => void;
    model_id: string;
}): JSX.Element => {
    
    function onGridReady(params: GridReadyEvent) {
        if (window.gridApiMap === undefined) {
            window.gridApiMap = new Map();
        }
        window.gridApiMap.set(props.model_id, params.api);
    }

    const cellValueChanged = (e : CellValueChangedEvent) => {
        const column = e.colDef.field ? e.colDef.field : "";
        const newValue = e.newValue;
        
        props.sendCellValueUpdate(column, newValue);
    };

    const columns = buildGridColumns(props.sheetJSON.columns, props.setEditingMode);
    const rowData = buildGridData(props.sheetJSON);

    const frameworkComponents={
        simpleEditor: MitoCellEditor
    }

    return (
        <div>
            <div className="ag-theme-alpine ag-grid"> 
                <AgGridReact
                    onGridReady={onGridReady}
                    onCellFocused={(e : CellFocusedEvent) => props.cellFocused(e)}
                    rowData={rowData}
                    frameworkComponents={frameworkComponents}
                    onCellValueChanged={cellValueChanged} >
                    {columns}
                </AgGridReact>
            </div>
        </div>
    );
};

export default MitoSheet;