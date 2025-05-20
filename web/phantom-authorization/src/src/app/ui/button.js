export function Button({ children, className = '', ...props }) {
  return (
    <button
      type="submit"
      className={`
        rounded-md 
        bg-[#367467] 
        px-4 py-2 
        text-white
        transition 
        ${className}
      `}
      {...props}
    >
      {children}
    </button>
  );
}

