import React from 'react';

// import css
import "../../css/modal.css"
import "../../css/margins.css"

import { ModalEnum } from './Mito';


/*
    DefaultModal is a higher-order component that
    takes a modal and a header, and displays it as a component.
*/
const DefaultModal = (
    props : {
        header: string;
        viewComponent: React.ReactFragment;
        setModal: (modal: ModalEnum) => void;
    }): JSX.Element => {

    return (
        <div className='modal-container'>
            <div className='modal'>
                {/* Note: we close whenever you click anywhere on the header! */}
                <div className='modal-header' onClick={() => {props.setModal(ModalEnum.None)}}>
                    <div className='modal-header-text'>{props.header}</div>
                    <div className='modal-header-close'>X</div>
                </div>
                {props.viewComponent}
            </div> 
        </div>
    )

};

export default DefaultModal;