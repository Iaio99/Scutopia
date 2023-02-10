import { Author } from "./author";

export interface Publication {
    eid: string;
    //authors: Author[];
    title: string;
    pubblicationDate: string;
    magazine: string;
    volume: number;
    page_range: string;
    doi: string;
    download_date: Date;
    scopus_id: string;
}