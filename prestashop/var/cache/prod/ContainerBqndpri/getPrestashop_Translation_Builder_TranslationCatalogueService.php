<?php

use Symfony\Component\DependencyInjection\Argument\RewindableGenerator;

// This file has been auto-generated by the Symfony Dependency Injection Component for internal use.
// Returns the public 'prestashop.translation.builder.translation_catalogue' shared service.

return $this->services['prestashop.translation.builder.translation_catalogue'] = new \PrestaShop\PrestaShop\Core\Translation\Builder\TranslationCatalogueBuilder(${($_ = isset($this->services['prestashop.translation.provider.catalogue_provider_factory']) ? $this->services['prestashop.translation.provider.catalogue_provider_factory'] : $this->load('getPrestashop_Translation_Provider_CatalogueProviderFactoryService.php')) && false ?: '_'});