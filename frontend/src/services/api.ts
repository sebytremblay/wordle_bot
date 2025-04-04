import { NewGameResponse, GuessResponse } from '../types/game';
import { SolverInfo, HintResponse } from '../types/hint';
import { logger } from '../utils/logger';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

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

export async function startNewGame(
    solver: string = 'naive'
): Promise<NewGameResponse> {
    return makeRequest<NewGameResponse>('/newgame', {
        method: 'POST',
        body: JSON.stringify({ solver }),
    });
}

export async function submitGuess(
    gameId: string,
    guess: string
): Promise<GuessResponse> {
    return makeRequest<GuessResponse>('/guess', {
        method: 'POST',
        body: JSON.stringify({ game_id: gameId, guess }),
    });
}

export async function getHint(
    gameId: string,
    solver?: string
): Promise<HintResponse> {
    const params = new URLSearchParams({ game_id: gameId });
    if (solver) {
        params.append('solver', solver);
    }
    return makeRequest<HintResponse>(`/hint?${params.toString()}`, {
        method: 'GET'
    });
}

export async function getSolvers(): Promise<{ solvers: SolverInfo[] }> {
    return makeRequest<{ solvers: SolverInfo[] }>('/solvers', {
        method: 'GET'
    });
} 