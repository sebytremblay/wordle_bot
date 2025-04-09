import React, { useState } from 'react';
import WordListPopup from '@/components/WordListPopup';
import { Counter } from '@/styles/components/WordListCounter.styles';

interface WordListCounterProps {
    count: number;
    gameId: string;
}

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
            <Counter onClick={handleClick} type="button">
                {isLoading ? (
                    'Loading...'
                ) : (
                    <>
                        <span>
                            {count === 1 ? 'Only 1 word remaining!' : `${count} possible words remaining`}
                        </span>
                        <span role="img" aria-label="click to view">🔍</span>
                    </>
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