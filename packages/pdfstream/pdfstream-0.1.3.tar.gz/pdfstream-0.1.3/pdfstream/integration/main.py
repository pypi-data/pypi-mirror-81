import typing as tp

import numpy as np
from numpy import ndarray
from pyFAI import AzimuthalIntegrator

from pdfstream.integration.tools import bg_sub, auto_mask, vis_img, integrate, vis_chi


def get_chi(
    ai: AzimuthalIntegrator,
    img: ndarray,
    bg_img: ndarray = None,
    bg_scale: float = None,
    mask_setting: dict = None,
    integ_setting: dict = None,
    img_setting: dict = None,
    plot_setting: dict = None
) -> tp.Tuple[
    ndarray,
    dict,
    ndarray,
    tp.Union[None, ndarray],
    tp.Union[str, dict]
]:
    """Process the diffraction image to get I(Q).

    The image will be subtracted by the background image and then auto masked. The results will be
    binned on the azimuthal direction and the average value of the intensity in the bin and their
    corresponding Q will be returned. The I(Q) and background subtracted masked image will
    be visualized.

    Parameters
    ----------
    ai : AzimuthalIntegrator
        The AzimuthalIntegrator.

    img : ndarray
        The of the 2D array of the image.

    bg_img : ndarray
        The 2D array of the background image. If None, no background subtraction.

    bg_scale : float
        The scale for background subtraction. If None, use 1.

    mask_setting : dict
        The auto mask setting.
        If None, use _AUTOMASK_SETTING in the tools module. To turn off the auto masking, use "OFF".

    integ_setting : dict
        The integration setting.
        If None, use _INTEG_SETTING in the tools module.

    img_setting : dict
        The user's modification to imshow kwargs except a special key 'z_score'. If None, use use empty dict.
        To turn off the imshow, use "OFF".

    plot_setting : dict
        The kwargs for the plot function. If None, use empty dict.

    Returns
    -------
    chi : ndarray
        The 2D array of integrated results. The first row is the Q and the second row is the I.

    _integ_setting: dict
        The integration setting used.

    img : ndarray
        The background subtrated image. If no background subtraction, return the input image.

    mask : ndarray or None
        The mask array. If no auto_masking, return None.

    _mask_setting : dict or str
        The auto masking seeting.
    """
    if bg_img is not None:
        img = bg_sub(img, bg_img, bg_scale=bg_scale)
    if mask_setting != "OFF":
        mask, _mask_setting = auto_mask(img, ai, mask_setting=mask_setting)
    else:
        mask, _mask_setting = None, None
    if img_setting != "OFF":
        vis_img(img, mask, img_setting=img_setting)
    chi, _integ_setting = integrate(img, ai, mask=mask, integ_setting=integ_setting)
    if plot_setting != "OFF":
        vis_chi(chi, plot_setting=plot_setting, unit=_integ_setting.get('unit'))
    return chi, _integ_setting, img, mask, _mask_setting


def avg_imgs(imgs: tp.Iterable[ndarray], weights: tp.Iterable[float] = None) -> ndarray:
    """Average the 2D images.

    Parameters
    ----------
    imgs : ndarray
        The 2D array of diffraction images.

    weights : an iterable of floats
        The weights for the images. If None, images will not be weighted when averaged.

    Returns
    -------
    avg_img : ndarray
        The averaged 2D image array.
    """
    return np.average(np.stack(tuple(imgs), axis=0), axis=0, weights=weights)
