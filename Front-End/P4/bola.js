import { Phi } from "./math-constants";

// export as named export and keep default for backwards compatibility
export const volume = (radius) => (4 / 3) * Phi * Number(radius) ** 3;

export default volume;