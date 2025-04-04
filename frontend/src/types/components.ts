import { GameState } from './game';

export interface GuessInputProps {
    onSubmit: (guess: string) => Promise<void>;
    disabled: boolean;
}

export interface HintPanelProps {
    gameId: string;
    disabled: boolean;
}

export interface GameBoardProps {
    state: GameState;
} 