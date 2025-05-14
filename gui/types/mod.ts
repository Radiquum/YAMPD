import { ModFile } from "./file";

export type Mod = {
    "slug": string,
    "project_id": string;
    "icon": string,
    "title":string,
    "developers": string[],
    "source": string,
    "url": string,
    "environment": {
        "client": boolean,
        "server": boolean,
    },
    "dependencies": Mod[],
    "file": ModFile,
}