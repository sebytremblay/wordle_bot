import React from 'react';
import styled from '@emotion/styled';

interface WordListPopupProps {
    isOpen: boolean;
    onClose: () => void;
    words: string[];
}

const Overlay = styled.div`
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
`;

const PopupContent = styled.div`
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    max-width: 90%;
    width: 500px;
    max-height: 80vh;
    position: relative;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
`;

const CloseButton = styled.button`
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: #666;
    &:hover {
        color: #333;
    }
`;

const Title = styled.h2`
    margin-top: 0;
    margin-bottom: 20px;
    color: #333;
    font-size: 1.5rem;
`;

const WordList = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 10px;
    max-height: calc(80vh - 100px);
    overflow-y: auto;
    padding: 10px;
    
    &::-webkit-scrollbar {
        width: 8px;
    }
    
    &::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    &::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
`;

const Word = styled.div`
    padding: 8px;
    background-color: #f8f9fa;
    border-radius: 4px;
    text-align: center;
    font-family: monospace;
    color: #538d4e;
`;

const WordListPopup: React.FC<WordListPopupProps> = ({ isOpen, onClose, words }) => {
    if (!isOpen) return null;

    return (
        <Overlay onClick={onClose}>
            <PopupContent onClick={e => e.stopPropagation()}>
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