import React from 'react';

// Import CSS
import "../../css/mito-toolbar.css"

// Import Types
import { SheetJSON } from '../widget';
import { ModalEnum } from './Mito';

const MitoToolbar = (
    props: {
        sheetJSON: SheetJSON, 
        send: any,
        setDocumentation: (documentationOpen: boolean) => void,
        selectedCell: string,
        setModal: (modal: ModalEnum) => void
    }): JSX.Element => {

    /* Adds a new column onto the end of a sheet, with A, B, C... as the name */
    const addColumn = () => {
        const newColumn = String.fromCharCode(65 + props.sheetJSON.columns.length);
        // Log the new column creation
        window.logger?.track({
            userId: window.user_id,
            event: 'column_added_log_event',
            properties: {
                column_header: newColumn
            }
        })
        // TODO: have to update these timestamps, etc to be legit
        props.send({
            'event': 'edit_event',
            'type': 'add_column',
            'id': '123',
            'timestamp': '456',
            'column_header': newColumn
        })
    }

    return (
        <div className='mito-toolbar-container'>
            <div className='mito-toolbar-item cell-indicator vertical-align-content'>
                <p className="selected-cell">{props.selectedCell}</p>
            </div>

            <button className='mito-toolbar-item vertical-align-content' onClick={addColumn}>
                <svg width="26" height="30" viewBox="0 0 11 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="7" height="12" fill="#FBFBFB" fill-opacity="0.65"/>
                    <rect y="4" width="7" height="4" fill="#C4C4C4"/>
                    <rect y="8" width="7" height="4" fill="white" fill-opacity="0.65"/>
                    <rect x="0.25" y="0.25" width="6.5" height="11.5" stroke="black" stroke-width="0.5"/>
                    <rect x="3.7608" y="3.08218" width="6.12552" height="1.53138" transform="rotate(-0.364619 3.7608 3.08218)" fill="#27AE60"/>
                    <rect width="6.12552" height="1.53138" transform="matrix(-0.00636375 -0.99998 -0.99998 0.00636375 7.61353 6.8862)" fill="#27AE60"/>
                </svg>
            </button>
            <button className='mito-toolbar-item' onClick={() => {props.setDocumentation(true)}}>
                Documentation
            </button>
            <button className='mito-toolbar-item vertical-align-content' onClick={() => {props.setModal(ModalEnum.RepeatAnalysis)}}>
                Repeat analysis
            </button>
            {/* add className mito-toolbar-item to a div below to add another toolbar item! */}
        </div>
    );
};

export default MitoToolbar;