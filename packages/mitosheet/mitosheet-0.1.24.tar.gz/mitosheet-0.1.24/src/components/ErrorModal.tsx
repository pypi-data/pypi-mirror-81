// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, {Fragment} from 'react';
import { ErrorJSON } from '../widget';

// import css
import "../../css/margins.css"

import DefaultModal from './DefaultModal'; 
import { ModalEnum } from './Mito';

/*
    A modal that displays error messages and gives
    users actions to recover.
*/
const ErrorModal = (
    props : {
        errorJSON : ErrorJSON, 
        setModal: (modal: ModalEnum) => void
    }): JSX.Element => {

    return (
        <DefaultModal
            header={"Oops! " + props.errorJSON.header}
            modalType={ModalEnum.Error}
            viewComponent={
                <Fragment>
                    <div>
                        {props.errorJSON.to_fix} 
                    </div>
                </Fragment>
            }
            buttons={
                <Fragment>
                    <div className='modal-close-button modal-dual-button-left' onClick={() => {props.setModal(ModalEnum.None)}}> Close </div>
                    <div className='modal-action-button modal-dual-button-right' onClick={() => {
                            window.open("mailto:aarondr77@gmail.com", '_blank');
                            props.setModal(ModalEnum.None);
                        }}> {"Contact Us"}
                    </div>
                </Fragment> 
            }
        />
    )    
};

export default ErrorModal;