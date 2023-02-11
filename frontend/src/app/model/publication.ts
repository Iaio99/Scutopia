import { Author } from "./author";

export interface Publication {
    eid: string;
    authors: string;
    title: string;
    pubblicationDate: string;
    magazine: string;
    volume: number;
    page_range: string;
    doi: string;
    download_date: Date;
    scopus_id: string;
}