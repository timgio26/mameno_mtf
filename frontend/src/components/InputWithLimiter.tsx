import { useEffect, useState } from "react";

type InputWithLimiterProp = {
    functionAfterDelay: (val: string) => void;
    placeholder:string|undefined
}

export function InputWithLimiter({functionAfterDelay,placeholder}:InputWithLimiterProp){
    const [input, setInput] = useState<string>("");
    useEffect(() => {
        const timer = setTimeout(() => {
          if (input.length == 0 || input.length >= 3) {
            functionAfterDelay(input)
          }
        }, 500); // run this code after 500 ms
        return () => clearTimeout(timer); // cancel previous timer
      }, [input]);

    return(
        <input
            type="text"
            placeholder={placeholder}
            className="bg-transparent outline-none text-sm text-gray-700 w-40 sm:w-64"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
    )
}