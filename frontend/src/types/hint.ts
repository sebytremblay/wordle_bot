import { GameState } from "./game";

export interface HintResponse {
    hint: string;
    solver_type: string;
    candidates_remaining: number;
    state: GameState;
}

export interface SolverInfo {
    id: string;
    name: string;
    description: string;
}