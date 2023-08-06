import React from 'react';

// Import CSS
import "../../css/mito-toolbar.css"

// Import Types
import { SheetJSON } from '../widget';
import { ModalEnum } from './Mito';

const MitoToolbar = (
    props: {
        sheetJSON: SheetJSON, 
        send: (msg: Record<string, unknown>) => void,
        setDocumentation: (documentationOpen: boolean) => void,
        selectedCell: string,
        setModal: (modal: ModalEnum) => void,
        model_id: string
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

    /* Saves the current file as as an exported analysis */
    const exportAnalysis = () => {
        // We export using the gridApi.
        window.gridApiMap?.get(props.model_id)?.exportDataAsCsv({
            fileName: 'mito-export'
        });
        props.setModal(ModalEnum.Export);
    }

    return (
        <div className='mito-toolbar-container'>
            <div className='mito-toolbar-item cell-indicator vertical-align-content'>
                <p className="selected-cell">{props.selectedCell}</p>
            </div>

            <button className='mito-toolbar-item vertical-align-content' onClick={addColumn}>
                <svg width="22" height="30" viewBox="0 0 8 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.45459 1V2.81818" stroke="#343434" strokeWidth="0.7" strokeLinecap="round"/>
                    <path d="M7.36365 1.90909L5.54547 1.90909" stroke="#343434" strokeWidth="0.7" strokeLinecap="round"/>
                    <path d="M6.45455 4.18182V6.90909V10.5455C6.45455 10.7965 6.25104 11 6 11H1.45455C1.20351 11 1 10.7965 1 10.5455V1.45455C1 1.20351 1.20351 1 1.45455 1H4.8961" stroke="#343434" strokeWidth="0.7"/>
                    <rect x="1" y="4.63635" width="5.45455" height="3.63636" fill="#343434" fillOpacity="0.19"/>
                </svg>
            </button>

            <button className='mito-toolbar-item vertical-align-content' onClick={exportAnalysis}>
                <svg width="22" height="25" viewBox="0 0 8 9" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1 5.74442V6.76108V7.77775H7.09999V5.74442" stroke="#343434" strokeWidth="0.7" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M4.0892 1.4863L4.0892 5.74441" stroke="#343434" strokeWidth="0.7" strokeLinecap="round"/>
                    <path d="M1.70752 2.94734C1.57376 3.08688 1.57845 3.30844 1.71799 3.4422C1.85754 3.57596 2.0791 3.57127 2.21286 3.43173L1.70752 2.94734ZM4.05898 0.999963L4.30819 0.754203C4.24181 0.686895 4.15103 0.6493 4.0565 0.649972C3.96197 0.650643 3.87173 0.689524 3.80631 0.757768L4.05898 0.999963ZM5.9691 3.43529C6.10483 3.57292 6.32643 3.57447 6.46406 3.43874C6.60169 3.30301 6.60324 3.08141 6.46751 2.94377L5.9691 3.43529ZM2.21286 3.43173L4.31165 1.24216L3.80631 0.757768L1.70752 2.94734L2.21286 3.43173ZM3.80978 1.24572L5.9691 3.43529L6.46751 2.94377L4.30819 0.754203L3.80978 1.24572Z" fill="#343434"/>
                </svg>
            </button>

            <button className='mito-toolbar-item vertical-align-content' onClick={() => {props.setModal(ModalEnum.RepeatAnalysis)}}>
                <svg width="30" height="25" viewBox="0 0 10 9" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M0.721922 6.41597C0.604528 6.56954 0.633853 6.7892 0.787421 6.90659C0.94099 7.02399 1.16065 6.99466 1.27804 6.8411L0.721922 6.41597ZM2.15097 5.12288L2.33273 4.82378C2.17986 4.73088 1.98155 4.7682 1.87291 4.91032L2.15097 5.12288ZM3.69 6.46771C3.85519 6.5681 4.07048 6.51556 4.17087 6.35037C4.27125 6.18519 4.21872 5.96989 4.05353 5.86951L3.69 6.46771ZM1.27804 6.8411L2.42903 5.33544L1.87291 4.91032L0.721922 6.41597L1.27804 6.8411ZM1.9692 5.42198L3.69 6.46771L4.05353 5.86951L2.33273 4.82378L1.9692 5.42198Z" fill="#343434"/>
                    <path d="M8.43646 4.57317C8.43646 6.33544 6.97439 7.76404 5.17084 7.76404C3.70861 7.76404 2.47084 6.825 2.05472 5.53043" stroke="#343434" strokeWidth="0.7"/>
                    <path d="M9.62537 2.40956C9.74276 2.25599 9.71344 2.03633 9.55987 1.91894C9.4063 1.80154 9.18664 1.83087 9.06925 1.98444L9.62537 2.40956ZM8.19632 3.70265L8.01456 4.00175C8.16743 4.09465 8.36574 4.05733 8.47438 3.91521L8.19632 3.70265ZM6.65729 2.35782C6.4921 2.25743 6.27681 2.30997 6.17642 2.47516C6.07604 2.64035 6.12857 2.85564 6.29376 2.95602L6.65729 2.35782ZM9.06925 1.98444L7.91826 3.49009L8.47438 3.91521L9.62537 2.40956L9.06925 1.98444ZM8.37809 3.40355L6.65729 2.35782L6.29376 2.95602L8.01456 4.00175L8.37809 3.40355Z" fill="#343434"/>
                    <path d="M1.91083 4.25237C1.91083 2.4901 3.3729 1.06149 5.17645 1.06149C6.63868 1.06149 7.87645 2.00053 8.29257 3.2951" stroke="#343434" strokeWidth="0.7"/>
                </svg>
            </button>

            <button className='mito-toolbar-item' onClick={() => {props.setDocumentation(true)}}>
                <svg width="25" height="25" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="7" cy="7" r="6.51" stroke="#404040" strokeWidth="0.98"/>
                    <path d="M7.27173 8.43865C7.2624 8.34531 7.2624 8.30798 7.2624 8.26131C7.2624 7.89731 7.38373 7.56131 7.67307 7.36531L8.1024 7.07598C8.64373 6.71198 9.0544 6.19865 9.0544 5.45198C9.0544 4.49998 8.31707 3.57598 7.0104 3.57598C5.57307 3.57598 4.94773 4.63065 4.94773 5.48931C4.94773 5.65731 4.9664 5.80665 5.00373 5.93731L5.90907 6.04931C5.87173 5.94665 5.84373 5.75065 5.84373 5.59198C5.84373 5.00398 6.1984 4.39731 7.0104 4.39731C7.75707 4.39731 8.12107 4.91065 8.12107 5.46131C8.12107 5.82531 7.94373 6.16131 7.6264 6.37598L7.21573 6.65598C6.66507 7.02931 6.44107 7.49598 6.44107 8.11198C6.44107 8.23331 6.44107 8.32665 6.4504 8.43865H7.27173ZM6.24507 9.77331C6.24507 10.1093 6.51573 10.38 6.85173 10.38C7.18773 10.38 7.46773 10.1093 7.46773 9.77331C7.46773 9.43731 7.18773 9.15731 6.85173 9.15731C6.51573 9.15731 6.24507 9.43731 6.24507 9.77331Z" fill="#343434"/>
                </svg>
            </button>
            {/* add className mito-toolbar-item to a div below to add another toolbar item! */}
        </div>
    );
};

export default MitoToolbar;