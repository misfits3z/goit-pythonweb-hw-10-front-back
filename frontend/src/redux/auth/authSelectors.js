

export const selectUsers = (state) => state.auth.users;
export const selectCurrentUser = (state) => state.auth.currentUser;
export const selectIsAuthenticated = (state) => !!state.auth.token;
export const selectAuthLoading = (state) => state.auth.isLoading;
export const selectAuthError = (state) => state.auth.error;
export const selectIsVerified = (state) => state.auth.isVerified;