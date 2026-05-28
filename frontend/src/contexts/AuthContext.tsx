import { createContext, ReactNode, useContext, useEffect, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";

import { authApi, LoginPayload } from "../api/auth";

const AUTH_SESSION_KEY = "pf_has_session";

function hasSessionHint() {
  try {
    return window.localStorage.getItem(AUTH_SESSION_KEY) === "1";
  } catch {
    return false;
  }
}

function updateSessionHint(hasSession: boolean) {
  try {
    if (hasSession) {
      window.localStorage.setItem(AUTH_SESSION_KEY, "1");
      return;
    }

    window.localStorage.removeItem(AUTH_SESSION_KEY);
  } catch {
    // Ignore storage access failures.
  }
}

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
  const [isCheckingSession, setIsCheckingSession] = useState(hasSessionHint);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    if (!isCheckingSession) {
      return;
    }

    const controller = new AbortController();

    async function checkSession() {
      try {
        await authApi.refresh(controller.signal);
        setIsAuthenticated(true);
      } catch {
        if (!controller.signal.aborted) {
          updateSessionHint(false);
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
  }, [isCheckingSession]);

  async function login(credentials: LoginPayload) {
    await authApi.login(credentials);
    updateSessionHint(true);
    setIsAuthenticated(true);
  }

  async function logout() {
    try {
      await authApi.logout();
    } finally {
      updateSessionHint(false);
      queryClient.clear();
      setIsAuthenticated(false);
    }
  }

  return (
    <AuthContext.Provider value={{ isCheckingSession, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth deve ser usado dentro de AuthProvider.");
  }

  return context;
}