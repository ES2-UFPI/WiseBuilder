export interface cpu {
    id: string,
    consumption: string,
    socket: string,
    cores: number,
    clock_base: number,
    clock_max: number,
    ram_max_clock: number,
    intergrated_gpu: string,
    overclock: boolean,
  }