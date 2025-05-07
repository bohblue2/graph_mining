// 기본 날짜 정보
export interface QueryInfo {
	from: string; // YYYY-MM-DD
	to: string; // YYYY-MM-DD
}

// 기업 노드
export interface CompanyNode {
	type: 'company';
	ISIN: string;
	name: string;
	priceFrom: number;
	priceTo: number;
	priceChange: number;
	currency: string;
	market: string;
	source: string;
}

// 키워드 노드
export interface KeywordNode {
	type: 'keyword';
	keyword: string;
	priceChange: number;
}

// 엣지 정보 (회사 ↔ 키워드)
export interface Edge {
	source: string; // 회사 이름
	target: string; // 키워드
	weight: number; // 0 ~ 1 사이의 연결 강도
}

// 전체 구조
export interface CompanyKeywordGraph {
	query_info: QueryInfo;
	company_nodes: CompanyNode[];
	keyword_nodes: KeywordNode[];
	edges: Edge[];
}
