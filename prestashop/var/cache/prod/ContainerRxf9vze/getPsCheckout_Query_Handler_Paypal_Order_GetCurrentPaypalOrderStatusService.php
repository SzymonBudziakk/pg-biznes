<?php

use Symfony\Component\DependencyInjection\Argument\RewindableGenerator;

// This file has been auto-generated by the Symfony Dependency Injection Component for internal use.
// Returns the public 'ps_checkout.query.handler.paypal.order.get_current_paypal_order_status' shared service.

return $this->services['ps_checkout.query.handler.paypal.order.get_current_paypal_order_status'] = new \PrestaShop\Module\PrestashopCheckout\PayPal\Order\QueryHandler\GetCurrentPayPalOrderStatusQueryHandler(${($_ = isset($this->services['ps_checkout.repository.pscheckoutcart']) ? $this->services['ps_checkout.repository.pscheckoutcart'] : $this->load('getPsCheckout_Repository_PscheckoutcartService.php')) && false ?: '_'});
