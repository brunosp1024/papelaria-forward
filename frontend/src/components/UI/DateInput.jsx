
import ReactDatePicker, { registerLocale } from "react-datepicker";
import ptBR from "date-fns/locale/pt-BR";
import "react-datepicker/dist/react-datepicker.css";
import "./DateInput.css";

registerLocale("pt-BR", ptBR);

const DateInput = ({ label, value, onChange, min, max, ...props }) => {
    return (
        <label className="date-input__field">
            <span className="date-input__label">{label}</span>
            <ReactDatePicker
                className="date-input__input"
                calendarClassName="date-input__calendar"
                portalId="date-input-portal"
                popperPlacement="bottom-start"
                popperProps={{ strategy: "fixed" }}
                selected={value}
                onChange={onChange}
                dateFormat="dd/MM/yyyy"
                locale="pt-BR"
                placeholderText="dd/mm/aaaa"
                minDate={min}
                maxDate={max}
                showMonthDropdown
                showYearDropdown
                dropdownMode="select"
                {...props}
            />
            <span className="date-input__icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="3" y="5" width="18" height="16" rx="2" stroke="#1976d2" strokeWidth="1.5"/>
                    <path d="M16 3V7" stroke="#1976d2" strokeWidth="1.5" strokeLinecap="round"/>
                    <path d="M8 3V7" stroke="#1976d2" strokeWidth="1.5" strokeLinecap="round"/>
                    <path d="M3 11H21" stroke="#1976d2" strokeWidth="1.5"/>
                </svg>
            </span>
        </label>
    );
};

export default DateInput;
