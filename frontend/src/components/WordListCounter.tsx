import React, { useState } from 'react';
import styled from '@emotion/styled';
import WordListPopup from './WordListPopup';

interface WordListCounterProps {
    count: number;
    gameId: string;
}

const Counter = styled.div`
    max-width: 350px;
    margin: 10px auto;
    padding: 10px;
    background-color: #f8f9fa;
    border-radius: 4px;
    text-align: center;
    font-size: 1.1rem;
    color: #538d4e;
    cursor: pointer;
    transition: background-color 0.2s;

    &:hover {
        background-color: #e9ecef;
    }
`;

const WordListCounter: React.FC<WordListCounterProps> = ({ count, gameId }) => {
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const [words, setWords] = useState<string[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    const handleClick = async () => {
        if (!isLoading) {
            setIsLoading(true);
            try {
                const response = await fetch(`${process.env.REACT_APP_API_URL}/remaining-words?game_id=${gameId}`);
                const data = await response.json();
                if (response.ok) {
                    setWords(data.words);
                    setIsPopupOpen(true);
                } else {
                    console.error('Failed to fetch remaining words:', data.error);
                }
            } catch (error) {
                console.error('Error fetching remaining words:', error);
            } finally {
                setIsLoading(false);
            }
        }
    };

    return (
        <>
            <Counter onClick={handleClick}>
                {isLoading ? 'Loading...' : (
                    count === 1 ? 'Only 1 word remaining!' : `${count} possible words remaining`
                )}
            </Counter>
            <WordListPopup
                isOpen={isPopupOpen}
                onClose={() => setIsPopupOpen(false)}
                words={words}
            />
        </>
    );
};

export default WordListCounter; 