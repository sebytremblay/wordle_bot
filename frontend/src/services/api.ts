import { NewGameResponse, GuessResponse, GameState } from '../types/game';
import { SolverInfo, HintResponse } from '../types/hint';
import { logger } from '../utils/logger';
import { SolversResponse } from '../types/solvers';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

export class ApiError extends Error {
    constructor(
        message: string,
        public status?: number,
        public data?: any
    ) {
        super(message);
        this.name = 'ApiError';
    }
}

async function handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new ApiError(
            errorData?.error || 'An error occurred',
            response.status,
            errorData
        );
    }

    return response.json();
}

async function makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
): Promise<T> {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        });

        return handleResponse<T>(response);
    } catch (error) {
        logger.error('API', `Request failed: ${endpoint}`, error);
        throw error instanceof ApiError
            ? error
            : new ApiError('Network error occurred');
    }
}

export const startNewGame = async (solver?: string): Promise<{ game_id: string; state: GameState }> => {
    const response = await fetch(`${API_BASE_URL}/newgame`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ solver }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to start new game');
    }

    return response.json();
};

export const startMirrorGame = async (gameId: string, solver?: string): Promise<{ game_id: string; state: GameState }> => {
    const response = await fetch(`${API_BASE_URL}/mirrorgame`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ game_id: gameId, solver }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to start mirror game');
    }

    return response.json();
};

export const submitGuess = async (gameId: string, guess: string): Promise<{ feedback: number[]; state: GameState }> => {
    const response = await fetch(`${API_BASE_URL}/guess`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ game_id: gameId, guess }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to submit guess');
    }

    return response.json();
};

export const getHint = async (gameId: string, solver: string): Promise<{ hint: string }> => {
    const response = await fetch(`${API_BASE_URL}/hint?game_id=${gameId}&solver=${solver}`);

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to get hint');
    }

    return response.json();
};

export const getSolvers = async (): Promise<SolversResponse> => {
    const response = await fetch(`${API_BASE_URL}/solvers`);

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to get solvers');
    }

    return response.json();
};

export const getRemainingWords = async (gameId: string): Promise<{ words: string[]; count: number }> => {
    const response = await fetch(`${API_BASE_URL}/remaining-words?game_id=${gameId}`);

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to get remaining words');
    }

    return response.json();
}; 