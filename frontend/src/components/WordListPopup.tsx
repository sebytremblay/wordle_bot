import React from 'react';
import {
    Overlay,
    PopupContent,
    CloseButton,
    Title,
    WordList,
    Word
} from '@/styles/components/WordListPopup.styles';

interface WordListPopupProps {
    isOpen: boolean;
    onClose: () => void;
    words: string[];
}

const WordListPopup: React.FC<WordListPopupProps> = ({ isOpen, onClose, words }) => {
    if (!isOpen) return null;

    return (
        <Overlay onClick={onClose}>
            <PopupContent onClick={(e: React.MouseEvent) => e.stopPropagation()}>
                <CloseButton onClick={onClose}>&times;</CloseButton>
                <Title>Remaining Words ({words.length})</Title>
                <WordList>
                    {words.map((word, index) => (
                        <Word key={index}>{word}</Word>
                    ))}
                </WordList>
            </PopupContent>
        </Overlay>
    );
};

export default WordListPopup; 