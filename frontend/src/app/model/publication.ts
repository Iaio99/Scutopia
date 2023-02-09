import { Author } from "./author";

export interface Publication {
    eid: string;
    authors: Author[];
    title: string;
    publicationDate: string;
    magazine: string;
    volume: number;
    pageRange: {
        start: number,
        end: number
    };
    doi: string;
    dateGot: Date;
    scopusID: string;
}
