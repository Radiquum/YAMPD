import { ModFile } from "./file";

export type Mod = {
    "slug": string,
    "icon": string,
    "title":string,
    "developers": string[],
    "source": string,
    "url": string,
    "environment": {
        "client": boolean,
        "server": boolean,
    },
    "file": ModFile,
}