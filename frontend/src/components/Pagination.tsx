import { CiSquareChevLeft, CiSquareChevRight } from "react-icons/ci";

type PaginationProp = {
  page: number;
  total_page: number;
  onPrev?: () => void;
  onNext?: () => void;
};

export function Pagination({ page, total_page, onPrev, onNext }: PaginationProp) {
  return (
    <div className="flex items-center justify-center gap-6 px-6 py-3 w-fit mx-auto">
      <button
        onClick={onPrev}
        disabled={page <= 1}
        className="text-slate-600 hover:text-blue-600 disabled:text-gray-300 transition"
      >
        <CiSquareChevLeft size={28} />
      </button>

      <span className="text-sm font-semibold text-gray-700 tracking-wide">
        Page <span className="text-blue-600">{page}</span> of {total_page}
      </span>

      <button
        onClick={onNext}
        disabled={page >= total_page}
        className="text-slate-600 hover:text-blue-600 disabled:text-gray-300 transition"
      >
        <CiSquareChevRight size={28} />
      </button>
    </div>
  );
}