"""
StarGAN v2
Copyright (c) 2020-present NAVER Corp.

This work is licensed under the Creative Commons Attribution-NonCommercial
4.0 International License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

import os
from os.path import join as ospj

import torch
import torch.nn as nn

from core.model import build_model
from core.checkpoint import CheckpointIO
from core.data_loader import InputFetcher
import core.utils as utils


class Solver(nn.Module):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.device = torch.device('cpu')

        self.nets_ema = build_model(args)
        # below setattrs are to make networks be children of Solver, e.g., for self.to(self.device)
        for name, module in self.nets_ema.items():
            setattr(self, name + '_ema', module)
        
        self.ckptios = [CheckpointIO(ospj(args.checkpoint_dir, '050000_nets_ema.ckpt'), data_parallel=False, **self.nets_ema)]
        
        self.to(self.device)

    def _load_checkpoint(self, step):
        for ckptio in self.ckptios:
            ckptio.load(step)

    def using_reference(self, loaders):
        args = self.args
        nets_ema = self.nets_ema
        os.makedirs(args.result_dir, exist_ok=True)
        self._load_checkpoint(args.resume_iter)

        src = next(InputFetcher(loaders.src, None, args.latent_dim, 'test'))
        ref = next(InputFetcher(loaders.ref, None, args.latent_dim, 'test'))

        fname = ospj(args.result_dir, 'reference')
        print('Working on {}...'.format(fname))
        self.translate_using_reference(nets_ema, args, src.x, ref.x, ref.y, fname)

    def translate_using_reference(self, nets, args, x_src, x_ref, y_ref, fname):
        N, C, H, W = x_src.size() 
        wb = torch.ones(1, C, H, W).to(x_src.device)
        x_src_with_wb = torch.cat([wb, x_src], dim=0)

        masks = nets.fan.get_heatmap(x_src) if args.w_hpf > 0 else None
        s_ref = nets.style_encoder(x_ref, y_ref) 
        s_ref_list = s_ref.unsqueeze(1).repeat(1, N, 1) 
        x_concat = [x_src_with_wb]

        for i, s_ref in enumerate(s_ref_list):
            x_fake = nets.generator(x_src, s_ref, masks=masks)
            utils.save_image(x_fake,1,f'{fname}_{i+1}.jpg')
            x_fake_with_ref = torch.cat([x_ref[i:i+1], x_fake], dim=0)
            x_concat += [x_fake_with_ref]

        x_concat = torch.cat(x_concat, dim=0)
