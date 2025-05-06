const API = process.env.NEXT_PUBLIC_API_URL || "/api";

type _PACK_ENDPOINT = {
  getPack: string;
  getPackImage: string;
  editPackImage: string;
};

type _PACKS_ENDPOINT = {
  getPacks: string;
  createPack: string;
  deletePack: string;
};

type _MOD_ENDPOINT = {
  addMod: string;
  deleteMod: string;
  deleteModBulk: string;
};

export const PACK_ENDPOINT = (endpoint: keyof _PACK_ENDPOINT, id: string) => {
  if (!id) {
    console.error(`ENDPOINT "${endpoint}" REQUIRES A PACK ID`);
    return "";
  }

  const _endpoints = {
    getPack: `${API}/pack/${id}`,
    getPackImage: `${API}/pack/${id}/image`,
    editPackImage: `${API}/pack/${id}/image/edit`,
  };
  return _endpoints[endpoint];
};

export const PACKS_ENDPOINT = (
  endpoint: keyof _PACKS_ENDPOINT,
  id?: string | null
) => {
  const requireID: string[] = ["deletePack"];
  if (requireID.includes(endpoint) && !id) {
    console.error(`ENDPOINT "${endpoint}" REQUIRES A PACK ID`);
    return "";
  }

  const _endpoints = {
    getPacks: `${API}/packs/all`,
    createPack: `${API}/packs/new`,
    deletePack: `${API}/packs/${id}/delete`,
  };
  return _endpoints[endpoint];
};

export const MOD_ENDPOINT = (
  endpoint: keyof _MOD_ENDPOINT,
  id: string,
  slug?: string | null
) => {
  if (!id) {
    console.error(`ENDPOINT "${endpoint}" REQUIRES A PACK ID`);
    return "";
  }

  const requireSlug: string[] = ["deleteMod"];
  if (requireSlug.includes(endpoint) && !slug) {
    console.error(`ENDPOINT "${endpoint}" REQUIRES A MOD SLUG`);
    return "";
  }

  const _endpoints = {
    addMod: `${API}/pack/${id}/mod/add`,
    deleteMod: `${API}/pack/${id}/mod/${slug}/delete`,
    deleteModBulk: `${API}/pack/${id}/mods/delete`,
  };
  return _endpoints[endpoint];
};

export const DOWNLOAD_ENDPOINT = {
  downloadPack: `${API}/download/pack`,
  downloadMods: `${API}/download/mods`
}