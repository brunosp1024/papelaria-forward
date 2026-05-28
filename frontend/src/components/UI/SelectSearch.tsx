import { ChangeEvent, KeyboardEvent, useEffect, useMemo, useRef, useState } from "react";
import "./SelectSearch.css";

export type SelectSearchOption = {
  value: string;
  label: string;
  [key: string]: any;
};

export type SelectSearchProps = {
  value: string;
  onChange: (option: SelectSearchOption | null) => void;
  onSearch?: (search: string) => void;
  options: SelectSearchOption[];
  placeholder?: string;
  loading?: boolean;
  disabled?: boolean;
  getOptionLabel?: (option: SelectSearchOption) => string;
  getOptionValue?: (option: SelectSearchOption) => string;
  noResultsText?: string;
};

export default function SelectSearch({
  value,
  onChange,
  onSearch,
  options,
  placeholder = "Selecione...",
  loading = false,
  disabled = false,
  getOptionLabel = (o) => o.label,
  getOptionValue = (o) => o.value,
  noResultsText = "Nenhum resultado encontrado.",
}: SelectSearchProps) {
  const [inputValue, setInputValue] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const selectedOption = useMemo(
    () => options.find((option) => getOptionValue(option) === value),
    [getOptionValue, options, value],
  );
  const hasSelection = Boolean(selectedOption);

  const filteredOptions = useMemo(() => {
    const normalizedSearch = inputValue.trim().toLowerCase();

    if (!normalizedSearch) {
      return options;
    }

    return options.filter((option) => getOptionLabel(option).toLowerCase().includes(normalizedSearch));
  }, [getOptionLabel, inputValue, options]);

  useEffect(() => {
    if (selectedOption) {
      setInputValue(getOptionLabel(selectedOption));
      return;
    }

    if (!value) {
      setInputValue("");
    }
  }, [getOptionLabel, selectedOption, value]);

  function handleInputChange(event: ChangeEvent<HTMLInputElement>) {
    if (hasSelection) {
      return;
    }

    const nextValue = event.target.value;

    setInputValue(nextValue);
    setIsOpen(true);
    onChange(null);
    onSearch?.(nextValue);
  }

  function handleSelect(option: SelectSearchOption) {
    setInputValue(getOptionLabel(option));
    onChange(option);
    setIsOpen(false);
  }

  function handleInputFocus() {
    if (hasSelection) {
      setIsOpen(false);
      return;
    }

    setIsOpen(true);
  }

  function handleInputBlur() {
    window.setTimeout(() => {
      setIsOpen(false);

      if (selectedOption) {
        setInputValue(getOptionLabel(selectedOption));
      }
    }, 120);
  }

  function handleKeyDown(event: KeyboardEvent<HTMLInputElement>) {
    if (hasSelection) {
      return;
    }

    if (event.key === "Enter" && filteredOptions.length > 0) {
      event.preventDefault();
      handleSelect(filteredOptions[0]);
      return;
    }

    if (event.key === "Escape") {
      setIsOpen(false);
    }
  }

  function handleClearSelection() {
    setInputValue("");
    onChange(null);
    onSearch?.("");

    window.setTimeout(() => {
      inputRef.current?.focus();
      setIsOpen(true);
    }, 0);
  }

  return (
    <div className="select-search">
      <input
        ref={inputRef}
        type="search"
        value={inputValue}
        onChange={handleInputChange}
        onFocus={handleInputFocus}
        onBlur={handleInputBlur}
        onKeyDown={handleKeyDown}
        placeholder={loading ? "Carregando..." : placeholder}
        disabled={disabled || loading}
        readOnly={hasSelection}
        autoComplete="off"
        className={`select-search__input${hasSelection ? " select-search__input--selected" : ""}`}
      />
      {hasSelection && !disabled && !loading ? (
        <button
          className="select-search__clear"
          type="button"
          onMouseDown={(event) => event.preventDefault()}
          onClick={handleClearSelection}
          aria-label="Limpar selecao"
        >
          x
        </button>
      ) : null}
      {isOpen && !loading && !hasSelection && (
        <div className="select-search__results">
          {filteredOptions.length > 0 ? (
            filteredOptions.slice(0, 8).map((option) => (
              <button
                className="select-search__result"
                key={getOptionValue(option)}
                type="button"
                onClick={() => handleSelect(option)}
              >
                {getOptionLabel(option)}
              </button>
            ))
          ) : (
            <p className="select-search__no-results">{noResultsText}</p>
          )}
        </div>
      )}
    </div>
  );
}
