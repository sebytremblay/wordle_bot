import { FeedbackType } from './common';

export interface GuessEntry {
    guess: string;
    feedback: FeedbackType[];
}

export interface GameStateData {
    game_over: boolean;
    game_won: boolean;
    max_guesses: number;
    history: GuessEntry[];
    current_row: number;
    candidates_remaining: number;
}

export interface GameState {
    state: GameStateData;
    game_id: string;
    message?: string;
    error?: string;
}

export interface NewGameResponse {
    game_id: string;
    solver_type: string;
    state: GameStateData;
}

export interface GuessResponse {
    feedback: FeedbackType[];
    state: GameStateData;
    game_id: string;
    message?: string;
    error?: string;
} 