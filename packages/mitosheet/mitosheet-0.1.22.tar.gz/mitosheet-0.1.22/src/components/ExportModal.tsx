import React, { Fragment } from 'react';

// import css
import "../../css/repeat-analysis-modal.css"

import { ModalEnum } from './Mito';

import DefaultModal from './DefaultModal';

/*
    A modal that pops up to alert users their file has
    been downloaded to their downloads folder!
*/
const ExportModal = (props : {setModal: (modal: ModalEnum) => void}): JSX.Element => {

    return (
        <DefaultModal
            header='Export'
            viewComponent= {
                <Fragment>
                    <p>
                        Your export has completed. Check your downloads folder!
                    </p>
                </Fragment>
            }
            setModal={props.setModal}
        />
    )
};

export default ExportModal;