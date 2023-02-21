import { Author } from "./author";

export interface Publication {
    eid: string;
    authors: string;
    eid__publication_date: string;
    eid__title: string;
    eid__magazine: string;
    eid__volume: number;
    eid__page_range: string;
    eid__doi: string;
    eid__download_date: string;
    scopus_id__ssd: string;
}