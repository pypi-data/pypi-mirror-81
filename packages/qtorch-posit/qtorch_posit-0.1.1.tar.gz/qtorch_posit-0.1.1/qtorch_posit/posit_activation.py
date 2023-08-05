__all__ = ["PositTanhModule","PositTanhModuleEnhanced","RefTanhModule","PositLinear", "PositConv2d"]
#Todo : implement sigmoid, rarely used in modern DNN
import torch
from typing import TypeVar, Union, Tuple
from qtorch_posit.quant import posit_sigmoid, posit_tanh, posit_tanh_enhanced, posit_quantize
class PositTanhModule(torch.nn.Module):
    def forward(self, input):
        return PositTanhFunction.apply(input)
        #return torch.tanh(input)
    
class PositTanhFunction(torch.autograd.Function):

    @staticmethod
    def forward(ctx, input):
        # replace posit_tanh_enhanced <> posit_tanh for different approx
        output = posit_tanh(input,nsize=16,es=0)
        ctx.save_for_backward(output)
        return output#input.clamp(min=0)

    @staticmethod
    def backward(ctx, grad_output):
        output, = ctx.saved_tensors
        #tanhx = top_data[i];
        #bottom_diff[i] = top_diff[i] * (1 - tanhx * tanhx);
        #grad_input = grad_output.clone()
        grad_input = grad_output*(1- output*output)
        return grad_input
    
class PositTanhModuleEnhanced(torch.nn.Module):
    def forward(self, input):
        return PositTanhFunctionEnhanced.apply(input)
    
class PositTanhFunctionEnhanced(torch.autograd.Function):

    @staticmethod
    def forward(ctx, input):
        output = posit_tanh_enhanced(input,nsize=16,es=0)
        ctx.save_for_backward(output)
        return output#input.clamp(min=0)

    @staticmethod
    def backward(ctx, grad_output):
        output, = ctx.saved_tensors
        grad_input = grad_output*(1- output*output)
        return grad_input
    

    
class RefTanhModule(torch.nn.Module):
    def forward(self, input):
        return torch.tanh(input)

#wrapper for torch.nn modules 
class PositLinear(torch.nn.Module):
    def __init__(self, in_features: int, out_features: int, bias: bool = True , nsize: int = 8, es: int = 2, scale : float = 1.0):
        super(PositLinear, self).__init__()
        self.main_comp = torch.nn.Linear(in_features, out_features, bias)
        self.nsize = nsize
        self.es = es 
        self.scale = scale
    def forward(self, input):
        input = posit_quantize(input, nsize=self.nsize, es=self.es, scale=self.scale)
        output = self.main_comp(input)
        return posit_quantize(output, nsize=16, es=self.es, scale=1.0)
        
class PositConv2d(torch.nn.Module):
    def __init__(
            self,
            in_channels: int,
            out_channels: int,
            kernel_size: Union[int, Tuple[int, int]],
            stride: Union[int, Tuple[int, int]] = 1,
            padding: Union[int, Tuple[int, int]] = 0,
            dilation: Union[int, Tuple[int, int]] = 1,
            groups: int = 1,
            bias: bool = True,
            padding_mode: str = 'zeros' , nsize: int = 8, es: int = 2, scale : float = 1.0):
        super(PositConv2d, self).__init__()
        self.main_comp = torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, dilation, groups, bias, padding_mode)
        self.nsize = nsize
        self.es = es 
        self.scale = scale
    def forward(self, input):
        input = posit_quantize(input, nsize=self.nsize, es=self.es, scale=self.scale)
        output = self.main_comp(input)
        return posit_quantize(output, nsize=16, es=self.es, scale=1.0)
        