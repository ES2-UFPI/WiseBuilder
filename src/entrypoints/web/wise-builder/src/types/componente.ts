export interface Componente {
  _id: string;
  type: string;
  manufacturer: string;
  price?: number;
  link?: string;
  socket?: string;
  n_cores?: number;
  chipset?: string;
  board_size?: number;
  n_ram_slots?: number;
  n_usb2?: number;
  n_usb3x?: number;
  n_vga?: number;
  n_display_port?: number;
  n_hdmi?: number;
  pcie_gen?: number;
  n_pcie_x1?: number;
  n_pcie_x4?: number;
  n_pcie_x8?: number;
  n_pcie_x16?: number;
  power?: number;
  rate?: number;
  modularity?: number;
  base_clock_spd?: number;
  boost_clock_spd?: number;
  consumption?: number;
  integrated_gpu?: string;
  overclock?: boolean;
  vram?: number;
  vram_spd?: number;
  model?: string;
  generation?: number;
  frequency?: number;
  storage?: number;
  io?: number;
  is_HDD?: boolean;
  rpm?: number;
  available?: boolean;
  sata?:number;
  memory_type?:number;
}
