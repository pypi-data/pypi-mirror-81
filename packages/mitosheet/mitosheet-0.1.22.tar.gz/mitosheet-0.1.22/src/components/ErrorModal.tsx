import React, {Fragment} from 'react';
import { ErrorJSON } from '../widget';

// import css
import "../../css/error.css"
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
            header={props.errorJSON.header}
            viewComponent= {
                <Fragment>
                    <div className='error-message'>
                        {props.errorJSON.to_fix} 
                    </div>
                </Fragment>
            }
            setModal={props.setModal}
        />
    )    
};

export default ErrorModal;