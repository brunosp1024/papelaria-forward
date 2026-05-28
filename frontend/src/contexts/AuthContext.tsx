import { createContext, ReactNode, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";

import { authApi, LoginPayload } from "../api/auth";

type AuthContextValue = {
  isCheckingSession: boolean;
  isAuthenticated: boolean;
  login: (credentials: LoginPayload) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

type AuthProviderProps = {
  children: ReactNode;
};

export function AuthProvider({ children }: AuthProviderProps) {
  const queryClient = useQueryClient();
  const [isCheckingSession, setIsCheckingSession] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const controller = new AbortController();

    async function checkSession() {
      try {
        await authApi.refresh(controller.signal);
        setIsAuthenticated(true);
      } catch {
        if (!controller.signal.aborted) {
          setIsAuthenticated(false);
        }
      } finally {
        if (!controller.signal.aborted) {
          setIsCheckingSession(false);
        }
      }
    }

    checkSession();

    return () => {
      controller.abort();
    };
  }, []);

  const login = useCallback(async (credentials: LoginPayload) => {
    await authApi.login(credentials);
    setIsAuthenticated(true);
  }, []);

  const logout = useCallback(async () => {
    try {
      await authApi.logout();
    } finally {
      queryClient.clear();
      setIsAuthenticated(false);
    }
  }, [queryClient]);

  const value = useMemo(
    () => ({ isCheckingSession, isAuthenticated, login, logout }),
    [isCheckingSession, isAuthenticated, login, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth deve ser usado dentro de AuthProvider.");
  }

  return context;
}