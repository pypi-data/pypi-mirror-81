import React, { Fragment, useState } from 'react';

// import css
import "../../css/repeat-analysis-modal.css"

import { ModalEnum } from './Mito';

import DefaultModal from './DefaultModal';

/*
    A modal that allows users to input a file path to 
    repeat the current analysis on that file, in a
    new Jupyter code cell.
*/
const RepeatAnalysisModal = (props : {setModal: (modal: ModalEnum) => void}): JSX.Element => {
    const [fileName, setFileName] = useState('');

    function onSubmit(e:  React.FormEvent<HTMLFormElement>) : void {
        e.preventDefault(); 
        window.commands?.execute('repeat-analysis', {fileName: fileName});
        props.setModal(ModalEnum.None);
    }

    return (
        <DefaultModal
            header='Repeat analysis'
            viewComponent= {
                <Fragment>
                    <form className='repeat-analysis-form' onSubmit={(e) => {onSubmit(e)}}>
                        <label>
                            <p>
                                File name to repeat analysis on:
                            </p>
                            <input type="text" placeholder='datafile2.csv' value={fileName} onChange={(e) => {setFileName(e.target.value)}} />
                        </label>
                        <input type="submit" value="Repeat Analysis" />
                    </form>
                </Fragment>
            }
            setModal={props.setModal}
        />
    )
};

export default RepeatAnalysisModal;