import { Mod } from "./mod";

export type Pack = {
  _id: string;
  formatVersion: number;
  modpackVersion: number;
  title: string;
  author: string;
  version: string;
  modloader: string;
  updateURL: "";
  mods: Mod[];
};
